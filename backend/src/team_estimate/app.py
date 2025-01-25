"""
team_estimate Lambda Function

This Lambda is triggered by API Gateway when a user submits a story for team estimation.
It creates estimates by:
1. Getting selected roles from settings
2. Spawning parallel worker Lambdas for each role
3. Collecting and aggregating responses
4. Storing results in the estimates table

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

def invoke_worker_lambda(role: str, story_data: dict) -> dict:
    """
    Invokes a worker Lambda for a specific role to get their estimate.
    
    Args:
        role (str): The role ID (e.g., 'senior_dev', 'qa_engineer')
        story_data (dict): Story content and context
        
    Returns:
        dict: The worker's response containing their estimate
    """
    try:
        payload = {
            'role': role,
            'story_data': story_data
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

def calculate_average_estimate(estimates: list) -> dict:
    """
    Calculates the average estimate and confidence across all roles.
    
    Args:
        estimates (list): List of role estimates
        
    Returns:
        dict: Average estimate and confidence
    """
    total_estimate = sum(float(e['estimate']) for e in estimates)
    total_confidence = sum(float(e['confidence']) for e in estimates)
    count = len(estimates)
    
    return {
        'average_estimate': Decimal(str(total_estimate / count)),
        'average_confidence': Decimal(str(total_confidence / count))
    }

def handler(event, context):
    """
    Main handler for team estimation process.
    
    Args:
        event (dict): API Gateway event containing:
            story_id (str): Story UUID
            tenant_id (str): Tenant ID
            settings (dict): User's estimation settings
            content (dict): Story content
        context (obj): Lambda context
    
    Returns:
        dict: API Gateway response with estimation results
    """
    try:
        logger.info(f"Event received: {json.dumps(event)}")
        
        # Parse request
        body = json.loads(event['body'])
        story_id = body['story_id']
        tenant_id = body['tenant_id']  # Make sure this is passed from the frontend
        settings = body['settings']
        content = body['content']
        selected_roles = settings['selectedRoles']
        
        # Get story data
        story_data = {
            'content': content,
            'settings': settings
        }
        
        estimates = []
        
        # Invoke worker Lambdas in parallel
        with ThreadPoolExecutor(max_workers=len(selected_roles)) as executor:
            future_to_role = {
                executor.submit(invoke_worker_lambda, role, story_data): role 
                for role in selected_roles
            }
            
            for future in as_completed(future_to_role):
                role = future_to_role[future]
                try:
                    estimate_data = future.result()
                    estimates.append(estimate_data)
                    store_estimate(story_id, role, estimate_data, tenant_id)
                except Exception as e:
                    logger.error(f"Error processing estimate for role {role}: {str(e)}")
                    raise
        
        # Calculate averages
        averages = calculate_average_estimate(estimates)
        
        # Store final results
        timestamp = datetime.utcnow().isoformat()
        final_result = {
            'story_id': story_id,
            'version': 'TEAM_ESTIMATES_COMPLETE',
            'estimates': estimates,
            'average_estimate': averages['average_estimate'],
            'average_confidence': averages['average_confidence'],
            'settings_used': settings,
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        stories_table.put_item(Item=final_result)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'story_id': story_id,
                'message': 'Team estimates completed',
                'estimates': estimates,
                'averages': averages
            })
        }
        
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 