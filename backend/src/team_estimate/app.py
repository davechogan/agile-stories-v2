"""
team_estimate Lambda Function

This Lambda is triggered by API Gateway when a user submits a story for team estimation.
It:
1. Fetches story from DynamoDB
2. Gets selected roles from settings
3. Spawns parallel worker Lambdas for each role
4. Collects and aggregates responses
5. Returns formatted results for frontend

Environment Variables:
    DYNAMODB_TABLE (str): Name of the DynamoDB table for storing stories
    ESTIMATES_TABLE (str): Name of the DynamoDB table for storing estimates
    ENVIRONMENT (str): Environment name (e.g., 'dev', 'prod')
    WORKER_LAMBDA_ARN (str): ARN of the worker Lambda function
"""

import os
import json
import boto3
import logging
from datetime import datetime, UTC
from decimal import Decimal
import asyncio

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
lambda_client = boto3.client('lambda')

# Use the actual table name
ESTIMATES_TABLE = 'dev-agile-stories-estimations'  # or whatever your table name is

class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder for Decimal types"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)

def get_nearest_fibonacci(num: Decimal) -> Decimal:
    """Get nearest Fibonacci number (1,2,3,5,8,13,21)"""
    fib_sequence = [Decimal('1'), Decimal('2'), Decimal('3'), Decimal('5'), 
                   Decimal('8'), Decimal('13'), Decimal('21')]
    if num <= Decimal('0'):
        return Decimal('1')
    return min(fib_sequence, key=lambda x: abs(x - num))

def calculate_confidence(estimates: list) -> str:
    """Conservative approach: if any LOW, return LOW, if any MEDIUM, return MEDIUM, else HIGH"""
    confidences = [est.get('confidence', 'LOW') for est in estimates]
    if 'LOW' in confidences:
        return 'LOW'
    elif 'MEDIUM' in confidences:
        return 'MEDIUM'
    return 'HIGH'

async def invoke_worker_lambda(role: str, story_data: dict, story_id: str, tenant_id: str) -> dict:
    """Invokes a worker Lambda for a specific role."""
    try:
        payload = {
            'role': role,
            'content': story_data,
            'story_id': story_id,
            'tenant_id': tenant_id
        }
        
        logger.info(f"Invoking worker lambda for role {role} with payload: {json.dumps(payload)}")
        
        response = lambda_client.invoke(
            FunctionName="dev-agile-stories-estimate-worker",
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        
        return json.loads(response['Payload'].read())
    except Exception as e:
        logger.error(f"Error invoking worker lambda for role {role}: {str(e)}")
        raise

def calculate_averages(estimates: list) -> dict:
    """Calculate average estimates with Fibonacci numbers for story points"""
    story_points = []
    person_days = []
    
    for est in estimates:
        if 'estimates' in est:
            sp = est['estimates'].get('story_points', {})
            pd = est['estimates'].get('person_days', {})
            
            if 'value' in sp:
                story_points.append(Decimal(str(sp['value'])))
            if 'value' in pd:
                person_days.append(Decimal(str(pd['value'])))
    
    # Calculate averages
    sp_avg = Decimal('0')
    pd_avg = Decimal('0')
    
    if story_points:
        sp_avg = get_nearest_fibonacci(sum(story_points) / len(story_points))
    if person_days:
        pd_avg = sum(person_days) / len(person_days)
    
    return {
        'story_points': {
            'value': sp_avg,
            'confidence': calculate_confidence([e['estimates']['story_points'] for e in estimates])
        },
        'person_days': {
            'value': pd_avg,
            'confidence': calculate_confidence([e['estimates']['person_days'] for e in estimates])
        }
    }

def convert_to_decimal(obj):
    """Recursively convert any float or string number values to Decimal in a nested structure."""
    if isinstance(obj, dict):
        return {key: convert_to_decimal(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_decimal(item) for item in obj]
    elif isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, str):
        try:
            # Try to convert string to Decimal if it looks like a number
            return Decimal(obj)
        except:
            return obj
    return obj

def prepare_story_payload(story_data: dict) -> dict:
    """
    Prepares a simplified story payload for the workers.
    Extracts fields from content and analysis at root level.
    
    Args:
        story_data (dict): Raw story data from DynamoDB
        
    Returns:
        dict: Cleaned story payload for workers
    """
    try:
        content = story_data.get('content', {})
        analysis = story_data.get('analysis', {})

        return {
            'title': content.get('title'),
            'story': content.get('story'),
            'acceptance_criteria': content.get('acceptance_criteria'),
            'implementation_details': analysis.get('ImplementationDetails')
        }
    except Exception as e:
        logger.error(f"Error preparing story payload: {str(e)}")
        raise

def handler(event, context):
    """Main Lambda handler that wraps async implementation."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_async_handler(event, context))

async def _async_handler(event, context):
    """Async implementation of handler logic."""
    try:
        # Parse request
        body = json.loads(event.get('body', '{}'))
        logger.info(f"Received request body: {json.dumps(body)}")
        
        story_id = body.get('story_id')
        tenant_id = body.get('tenant_id')
        
        # Get roles directly from the root level
        roles = body.get('roles', [])
        logger.info(f"Selected roles: {json.dumps(roles)}")
        
        if not roles:
            logger.error("No roles found in request")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No roles provided in request'})
            }
            
        # Prepare story data
        story_data = {
            'title': body.get('content', {}).get('title'),
            'story': body.get('content', {}).get('story'),
            'acceptance_criteria': body.get('content', {}).get('acceptance_criteria', []),
            'implementation_details': body.get('content', {}).get('implementation_details', [])
        }
        
        logger.info(f"Prepared story data for workers: {json.dumps(story_data)}")
        
        # Process estimates for each role
        tasks = [
            process_role_estimate(role, story_data, story_id, tenant_id)
            for role in roles
        ]
        estimates = await asyncio.gather(*tasks)

        # Calculate final estimate
        final_estimate = {
            'estimation_id': f"{story_id}_FINAL",
            'story_id': story_id,
            'tenantId': tenant_id,
            'created_at': datetime.now(UTC).isoformat(),
            'r#role': 'FINAL',
            'averages': calculate_averages(estimates),
            'individual_estimates': estimates
        }

        # Save final estimate
        table = dynamodb.Table(ESTIMATES_TABLE)
        table.put_item(Item=json.loads(json.dumps(final_estimate, cls=DecimalEncoder)))

        return {
            'statusCode': 200,
            'body': json.dumps(final_estimate, cls=DecimalEncoder)
        }

    except Exception as e:
        logger.error(f"Error in handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

async def process_role_estimate(role: str, story_data: dict, story_id: str, tenant_id: str) -> dict:
    """Process estimate for a single role."""
    try:
        response = await invoke_worker_lambda(role, story_data, story_id, tenant_id)
        estimate = json.loads(response['body'])
        
        # Convert any float or string number values to Decimal
        estimate = convert_to_decimal(estimate)
        
        # Ensure estimates values are Decimal
        if 'estimates' in estimate:
            for est_type in ['story_points', 'person_days']:
                if est_type in estimate['estimates']:
                    value = estimate['estimates'][est_type].get('value')
                    if value is not None:
                        estimate['estimates'][est_type]['value'] = Decimal(str(value))
        
        # Create estimate record with role
        estimate_record = {
            'r#role': role,
            'estimates': estimate['estimates'],
            'justification': estimate['justification']
        }
        
        # Save individual estimate
        table = dynamodb.Table(ESTIMATES_TABLE)
        table.put_item(Item={
            'estimation_id': f"{story_id}_{role}",
            'story_id': story_id,
            'tenantId': tenant_id,
            'created_at': datetime.now(UTC).isoformat(),
            **estimate_record
        })
        
        return estimate_record

    except Exception as e:
        logger.error(f"Error processing role {role}: {str(e)}")
        raise 