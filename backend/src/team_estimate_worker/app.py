"""
Team Estimate Worker Lambda

This module processes team estimates for user stories.
It handles estimate collection from Step Functions and updates results in DynamoDB.

Flow:
1. Receives estimates from Step Functions task
2. Processes team estimates
3. Stores estimate results in DynamoDB
4. Returns estimate status to Step Functions
"""

import json
import os
from datetime import datetime
import boto3
import openai

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def handler(event, context):
    try:
        # Get task token from Step Functions
        task_token = event.get('taskToken')
        
        # Get story details
        story_id = event['story_id']
        
        # Process team estimates (your existing estimation logic)
        estimate_result = {
            'status': 'ESTIMATED',
            'final_estimate': 5,
            'confidence_level': 'HIGH',
            'team_consensus': True,
            'estimation_notes': [
                'Based on similar password reset implementations',
                'Including security considerations',
                'Email service integration time'
            ],
            'breakdown': {
                'frontend': 2,
                'backend': 2,
                'testing': 1
            }
        }
        
        # Store estimate results
        estimate_item = {
            'story_id': story_id,
            'version': 'TEAM_ESTIMATE',
            'content': estimate_result,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Update DynamoDB
        table.put_item(Item=estimate_item)
        
        # Return result to Step Functions
        if task_token:
            sfn = boto3.client('stepfunctions')
            sfn.send_task_success(
                taskToken=task_token,
                output=json.dumps({
                    'story_id': story_id,
                    'status': 'ESTIMATED',
                    'estimate': estimate_result
                })
            )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'story_id': story_id,
                'message': 'Team estimation completed',
                'status': 'COMPLETED',
                'estimate': estimate_result
            })
        }
        
    except Exception as e:
        error_response = {
            'error': str(e),
            'story_id': event.get('story_id')
        }
        
        # Notify Step Functions of failure
        if task_token:
            sfn = boto3.client('stepfunctions')
            sfn.send_task_failure(
                taskToken=task_token,
                error='TeamEstimateWorkerError',
                cause=str(e)
            )
        
        return {
            'statusCode': 500,
            'body': json.dumps(error_response)
        } 