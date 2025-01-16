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

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
sfn = boto3.client('stepfunctions')

def handler(event, context):
    try:
        # Parse input
        body = json.loads(event['body']) if 'body' in event else event
        story_id = body.get('story_id', str(uuid.uuid4()))
        
        # Store original story
        original_item = {
            'story_id': story_id,
            'version': 'ORIGINAL',
            'content': {
                'title': body['title'],
                'description': body['description'],
                'acceptance_criteria': body['acceptance_criteria']
            },
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Store in DynamoDB
        table.put_item(Item=original_item)
        
        # Start Step Functions workflow
        workflow_input = {
            'story_id': story_id,
            'title': body['title'],
            'description': body['description'],
            'acceptance_criteria': body['acceptance_criteria']
        }
        
        # Start execution
        sfn.start_execution(
            stateMachineArn=os.environ['STEP_FUNCTION_ARN'],
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
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 