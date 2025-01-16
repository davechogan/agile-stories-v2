"""
Story Analysis Lambda Handler

This module handles the initial submission of user stories for analysis.
It stores the original story in DynamoDB and starts the Step Functions workflow.
"""

import json
import os
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
    try:
        response = ssm.get_parameter(
            Name=f"/{os.environ['ENVIRONMENT']}/step-functions/workflow-arn"
        )
        return response['Parameter']['Value']
    except Exception as e:
        logger.error(f"Error getting Step Functions ARN: {str(e)}")
        raise Exception(f"Failed to get Step Functions ARN: {str(e)}")

def handler(event, context):
    try:
        logger.info(f"Event received: {json.dumps(event)}")
        
        # Parse request body
        body = json.loads(event['body'])
        logger.info(f"Parsed body: {json.dumps(body)}")
        
        # Generate story ID
        story_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Store story in DynamoDB
        item = {
            'story_id': story_id,
            'title': body['title'],
            'description': body['description'],
            'story': body['story'],
            'acceptance_criteria': body['acceptance_criteria'],
            'status': 'SUBMITTED',
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        logger.info(f"Storing item in DynamoDB: {json.dumps(item)}")
        table.put_item(Item=item)
        
        # Get Step Functions ARN from SSM
        step_function_arn = get_step_function_arn()
        logger.info(f"Retrieved Step Functions ARN: {step_function_arn}")
        
        # Start Step Functions workflow
        workflow_input = {
            'story_id': story_id,
            'title': body['title'],
            'description': body['description'],
            'story': body['story'],
            'acceptance_criteria': body['acceptance_criteria']
        }
        
        logger.info(f"Starting Step Functions execution with input: {json.dumps(workflow_input)}")
        sfn.start_execution(
            stateMachineArn=step_function_arn,
            input=json.dumps(workflow_input)
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'story_id': story_id,
                'message': 'Story submitted for analysis',
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