"""
Story Analysis Lambda Handler

This module handles the initial submission of user stories for analysis.
It stores the original story in DynamoDB and starts the Step Functions workflow.
"""

import json
import os
import uuid
from datetime import datetime
import boto3

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
sfn = boto3.client('sfn')
ssm = boto3.client('ssm')

# Get DynamoDB table
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def handler(event, context):
    try:
        # Parse request body
        body = json.loads(event['body'])
        
        # Generate story ID
        story_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Store story in DynamoDB
        item = {
            'id': story_id,
            'title': body['title'],
            'description': body['description'],
            'story': body['story'],
            'acceptance_criteria': body['acceptance_criteria'],
            'status': 'SUBMITTED',
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        table.put_item(Item=item)
        
        # Start Step Functions workflow
        workflow_input = {
            'story_id': story_id,
            'title': body['title'],
            'description': body['description'],
            'story': body['story'],
            'acceptance_criteria': body['acceptance_criteria']
        }
        
        sfn.start_execution(
            stateMachineArn=ssm.get_parameter(
                Name=f"/{os.environ['ENVIRONMENT']}/step-functions/workflow-arn"
            )['Parameter']['Value'],
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
        print(f"Error: {str(e)}")  # Add logging
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 