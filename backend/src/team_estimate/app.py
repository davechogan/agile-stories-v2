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
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from decimal import Decimal

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
lambda_client = boto3.client('lambda')
ssm = boto3.client('ssm')

# Get DynamoDB tables
stories_table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
estimates_table = dynamodb.Table(os.environ['ESTIMATES_TABLE'])

def get_story(story_id: str, tenant_id: str) -> dict:
    """
    Fetches story details from DynamoDB.
    """
    try:
        response = stories_table.get_item(
            Key={
                'story_id': story_id,
                'tenantId': tenant_id
            }
        )
        return response['Item']
    except Exception as e:
        logger.error(f"Error fetching story {story_id}: {str(e)}")
        raise

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
            'story_id': story_data['story_id'],
            'tenantId': story_data['tenantId'],
            'title': content.get('title'),
            'story': content.get('story'),
            'acceptance_criteria': content.get('acceptance_criteria'),
            'implementation_details': analysis.get('ImplementationDetails')
        }
    except Exception as e:
        logger.error(f"Error preparing story payload: {str(e)}")
        raise

def invoke_worker_lambda(role: str, story_payload: dict) -> dict:
    """
    Invokes a worker Lambda for a specific role.
    """
    try:
        payload = {
            'role': role,
            'story_data': story_payload,
            'story_id': story_payload['story_id'],
            'tenant_id': story_payload['tenantId']
        }
        
        response = lambda_client.invoke(
            FunctionName=os.environ['WORKER_LAMBDA_ARN'],
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        
        return json.loads(response['Payload'].read())
    except Exception as e:
        logger.error(f"Error invoking worker lambda for role {role}: {str(e)}")
        raise

def store_estimate(story_id: str, role: str, estimate_data: dict, tenant_id: str):
    """
    Stores an individual role's estimate in DynamoDB.
    
    Args:
        story_id (str): The story's UUID
        role (str): The estimating role
        estimate_data (dict): The estimate details
        tenant_id (str): The tenant ID
    """
    try:
        timestamp = datetime.utcnow().isoformat()
        estimation_id = f"{story_id}_{role}"  # Create unique estimation ID
        
        item = {
            'estimation_id': estimation_id,  # hash key
            'story_id': story_id,           # range key
            'tenantId': tenant_id,          # for tenant-index GSI
            'role': role,
            'estimate': estimate_data['estimate'],
            'confidence': estimate_data['confidence'],
            'rationale': estimate_data['rationale'],
            'created_at': timestamp         # for story-created-index GSI
        }
        
        estimates_table.put_item(Item=item)
        
    except Exception as e:
        logger.error(f"Error storing estimate for role {role}: {str(e)}")
        raise

def calculate_average_estimates(estimates: list) -> dict:
    """
    Calculates average estimates and confidence for both story points and person days.
    """
    def calc_type_average(estimate_type: str) -> dict:
        values = [e['estimates'][estimate_type]['value'] for e in estimates]
        confidences = [e['estimates'][estimate_type]['confidence'] for e in estimates]
        
        # Map confidence levels to numbers for averaging
        confidence_map = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3}
        confidence_nums = [confidence_map[c] for c in confidences]
        
        avg_value = sum(values) / len(values)
        avg_confidence_num = sum(confidence_nums) / len(confidence_nums)
        
        # Map back to confidence level
        confidence_levels = {1: 'LOW', 2: 'MEDIUM', 3: 'HIGH'}
        avg_confidence = confidence_levels[round(avg_confidence_num)]
        
        return {
            'value': Decimal(str(avg_value)),
            'confidence': avg_confidence
        }

    return {
        'story_points': calc_type_average('story_points'),
        'person_days': calc_type_average('person_days')
    }

def store_final_estimate(story_id: str, tenant_id: str, estimates: list):
    """
    Stores the final combined estimate data with both story points and person days.
    """
    try:
        timestamp = datetime.utcnow().isoformat()
        estimation_id = f"{story_id}_final"  # Special ID for combined record
        
        # Calculate averages for both types
        averages = calculate_average_estimates(estimates)
        
        item = {
            'estimation_id': estimation_id,
            'story_id': story_id,
            'tenantId': tenant_id,
            'version': 'FINAL',
            'created_at': timestamp,
            'averages': {
                'story_points': averages['story_points'],
                'person_days': averages['person_days']
            },
            'individual_estimates': estimates
        }
        
        estimates_table.put_item(Item=item)
        
    except Exception as e:
        logger.error(f"Error storing final estimate: {str(e)}")
        raise

def handler(event, context):
    try:
        # Parse request
        body = json.loads(event.get('body', '{}'))
        story_id = body.get('story_id')
        tenant_id = body.get('tenant_id')
        roles = body.get('roles', [])
        
        current_time = datetime.utcnow().isoformat()
        
        # Save original content in PENDING to stories table
        pending_item = {
            'story_id': story_id,
            'version': 'TEAM_ESTIMATE_PENDING',
            'tenant_id': tenant_id,
            'created_at': current_time,
            'updated_at': current_time,
            'content': {  # Original story content
                'title': body.get('content', {}).get('title', ''),
                'story': body.get('content', {}).get('story', ''),
                'acceptance_criteria': body.get('content', {}).get('acceptance_criteria', [])
            },
            'analysis': {  # Implementation details from tech review
                'ImplementationDetails': body.get('analysis', {}).get('ImplementationDetails', [])
            }
        }
        
        # Save PENDING version to stories table
        stories_table.put_item(Item=pending_item)
        
        # Invoke workers and collect results
        lambda_client = boto3.client('lambda')
        worker_results = []
        
        for role in roles:
            worker_payload = {
                'story_id': story_id,
                'tenant_id': tenant_id,
                'role': role,
                'content': pending_item['content'],
                'analysis': pending_item['analysis']
            }
            
            response = lambda_client.invoke(
                FunctionName='dev-agile-stories-estimate-worker',
                InvocationType='RequestResponse',  # Synchronous invocation
                Payload=json.dumps(worker_payload)
            )
            
            result = json.loads(response['Payload'].read())
            worker_results.append(result)
        
        # Calculate averages and store final estimate
        final_estimate = {
            'estimation_id': f"{story_id}_final",
            'story_id': story_id,
            'tenant_id': tenant_id,
            'version': 'FINAL',
            'created_at': datetime.utcnow().isoformat(),
            'averages': calculate_average_estimates(worker_results),
            'individual_estimates': worker_results
        }
        
        # Save final estimate to estimates table
        estimates_table.put_item(Item=final_estimate)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Estimation process completed',
                'story_id': story_id,
                'final_estimate': final_estimate
            })
        }
        
    except Exception as e:
        logger.error(f"Error in team estimate handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 