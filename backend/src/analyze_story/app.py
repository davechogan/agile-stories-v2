"""
analyze_story Lambda Function

This Lambda is triggered by API Gateway when a user submits a new story for analysis.
It creates the initial AGILE_COACH_PENDING version in DynamoDB and starts the Step Functions workflow.

Environment Variables:
    DYNAMODB_TABLE (str): Name of the DynamoDB table for storing stories
    ENVIRONMENT (str): Environment name (e.g., 'dev', 'prod')

Returns:
    dict: API Gateway response object
        statusCode (int): HTTP status code
        body (str): JSON string containing:
            story_id (str): UUID of the created story
            message (str): Success/error message
            status (str): Status of the operation
"""

import os
import json
import uuid
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
    """Lambda handler for analyzing stories."""
    try:
        # Parse the request body
        body = json.loads(event['body'])
        logger.info(f"Parsed body: \n{json.dumps(body, indent=4)}")
        
        tenant_id = body.get('tenant_id')
        token = body.get('token')
        
        # Add debug logging
        logger.info(f"Extracted token: {token}")
        logger.info(f"Extracted tenant_id: {tenant_id}")
        
        content = body.get('content')
        
        # Generate story ID
        story_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Debug print before creating item
        logger.info("Creating item with these values:")
        logger.info(f"- token: {token}")
        logger.info(f"- tenant_id: {tenant_id}")
        logger.info(f"- content: {json.dumps(content, indent=2)}")
        
        # Create initial story item
        item = {
            'story_id': story_id,
            'version': 'AGILE_COACH_PENDING',
            'tenant_id': tenant_id,
            'token': token,  # Verify this is being set
            'content': content,
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        # Debug print the item
        logger.info(f"Created item dictionary: \n{json.dumps(item, indent=4)}")
        
        logger.info(f"Storing story in DynamoDB: \n{json.dumps(item, indent=4)}")
        
        # Store in DynamoDB
        table.put_item(Item=item)
        
        # Verify what was stored
        response = table.get_item(
            Key={
                'story_id': story_id,
                'version': 'AGILE_COACH_PENDING'
            }
        )
        logger.info(f"Verified stored item: \n{json.dumps(response.get('Item'), indent=4)}")
        
        # Start Step Functions execution
        state_machine_arn = get_step_function_arn()
        execution_input = {
            'story_id': story_id,
            'token': token
        }
        
        logger.info(f"Starting Step Functions execution with input: {json.dumps(execution_input)}")
        
        sfn.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(execution_input)
        )
        
        # Return API Gateway formatted response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Add CORS header
            },
            'body': json.dumps({
                'story_id': story_id,
                'token': token
            })
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Add CORS header
            },
            'body': json.dumps({
                'error': str(e)
            })
        } 