"""
Technical Review Lambda Handler

This module handles technical review submissions.
It stores the review in DynamoDB and integrates with Step Functions workflow.

Flow:
1. Receives review from API Gateway or Step Functions
2. Stores review details in DynamoDB
3. Returns review status
4. Notifies Step Functions of task completion if called from workflow
"""

import json
import os
from datetime import datetime
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
sfn = boto3.client('stepfunctions')

def handler(event, context):
    try:
        # Get task token if exists (Step Functions invocation)
        task_token = event.get('taskToken')
        
        # Parse input (handle both API Gateway and Step Functions input)
        body = json.loads(event['body']) if 'body' in event else event
        story_id = body['story_id']
        
        # Store review submission
        review_item = {
            'story_id': story_id,
            'version': 'TECH_REVIEW_REQUEST',
            'content': {
                'reviewer': body.get('reviewer', 'system'),
                'review_notes': body.get('review_notes', ''),
                'status': 'SUBMITTED'
            },
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Store in DynamoDB
        table.put_item(Item=review_item)
        
        result = {
            'story_id': story_id,
            'message': 'Technical review submitted',
            'status': 'SUBMITTED'
        }
        
        # If called from Step Functions, send task success
        if task_token:
            sfn.send_task_success(
                taskToken=task_token,
                output=json.dumps(result)
            )
            return result
        
        # If called from API Gateway, return formatted response
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        error_response = {
            'error': str(e)
        }
        
        # If called from Step Functions, send task failure
        if task_token:
            sfn.send_task_failure(
                taskToken=task_token,
                error='TechnicalReviewError',
                cause=str(e)
            )
            return error_response
            
        # If called from API Gateway, return error response
        return {
            'statusCode': 500,
            'body': json.dumps(error_response)
        } 