"""
Team Estimate Lambda Handler

This module handles team estimation submissions.
It stores the estimates in DynamoDB and integrates with Step Functions workflow.

Flow:
1. Receives estimates from API Gateway or Step Functions
2. Stores estimate details in DynamoDB
3. Returns estimate status
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
        
        # Store estimate submission
        estimate_item = {
            'story_id': story_id,
            'version': 'TEAM_ESTIMATE_REQUEST',
            'content': {
                'estimator': body.get('estimator', 'system'),
                'estimate_value': body.get('estimate', 0),
                'confidence': body.get('confidence', 'MEDIUM'),
                'notes': body.get('notes', ''),
                'status': 'SUBMITTED'
            },
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Store in DynamoDB
        table.put_item(Item=estimate_item)
        
        result = {
            'story_id': story_id,
            'message': 'Team estimate submitted',
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
                error='TeamEstimateError',
                cause=str(e)
            )
            return error_response
            
        # If called from API Gateway, return error response
        return {
            'statusCode': 500,
            'body': json.dumps(error_response)
        } 