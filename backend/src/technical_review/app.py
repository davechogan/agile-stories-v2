"""
technical_review Lambda Function

This Lambda is triggered by API Gateway when a user submits a story for technical review.
It creates a SENIOR_DEV_PENDING version in DynamoDB and starts the Step Functions workflow.

Environment Variables:
    DYNAMODB_TABLE (str): Name of the DynamoDB table for storing stories
    ENVIRONMENT (str): Environment name (e.g., 'dev', 'prod')

Returns:
    dict: API Gateway response object
        statusCode (int): HTTP status code
        body (str): JSON string containing:
            story_id (str): UUID of the story
            message (str): Success/error message
            status (str): Status of the operation
"""

import os
import json
import boto3
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
sfn = boto3.client('stepfunctions')
ssm = boto3.client('ssm')

# Get DynamoDB table
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def get_step_function_arn():
    """
    Retrieves the Step Functions state machine ARN from SSM Parameter Store.
    
    Returns:
        str: The ARN of the Step Functions state machine
    
    Raises:
        Exception: If unable to retrieve the ARN from SSM
    """
    try:
        response = ssm.get_parameter(
            Name=f"/{os.environ['ENVIRONMENT']}/step-functions/workflow-arn"
        )
        return response['Parameter']['Value']
    except Exception as e:
        logger.error(f"Error getting Step Functions ARN: {str(e)}")
        raise Exception(f"Failed to get Step Functions ARN: {str(e)}")

def handler(event, context):
    """
    Lambda handler for processing technical review requests.
    
    Creates a new story version SENIOR_DEV_PENDING in DynamoDB with the user's
    edited content and starts the Step Functions workflow for technical review.
    
    Args:
        event (dict): API Gateway event object containing:
            body (str): JSON string with:
                story_id (str): UUID of the story
                content (dict): User's edited story content
                tenant_id (str, optional): Tenant identifier
        context (obj): Lambda context object
    
    Returns:
        dict: API Gateway response object
    
    Raises:
        Exception: For any processing errors
    """
    try:
        logger.info(f"Event received: {json.dumps(event)}")
        
        # Parse request body
        body = json.loads(event['body'])
        story_id = body['story_id']
        tenant_id = body.get('tenant_id', 'default')
        content = body['content']  # User's edited version after agile coach review
        timestamp = datetime.utcnow().isoformat()
        
        # Store the user's edited version as PENDING for tech review
        item = {
            'story_id': story_id,
            'version': 'SENIOR_DEV_PENDING',
            'tenant_id': tenant_id,
            'content': content,
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        logger.info(f"Storing user edited version in DynamoDB: {json.dumps(item)}")
        table.put_item(Item=item)
        
        # Start Step Functions workflow
        workflow_input = {
            'story_id': story_id,
            'tenant_id': tenant_id,
            'content': content
        }
        
        # Get Step Functions ARN and start execution
        step_function_arn = get_step_function_arn()
        logger.info(f"Starting Step Functions execution with input: {json.dumps(workflow_input)}")
        sfn.start_execution(
            stateMachineArn=step_function_arn,
            input=json.dumps(workflow_input)
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'story_id': story_id,
                'message': 'Story sent for technical review',
                'status': 'SUBMITTED'
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