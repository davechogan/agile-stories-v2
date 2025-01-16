"""
Technical Review Worker Lambda

This module processes technical reviews of user stories.
It handles review analysis from Step Functions and updates results in DynamoDB.

Flow:
1. Receives review from Step Functions task
2. Processes technical review
3. Stores review results in DynamoDB
4. Returns review status to Step Functions
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
        
        # Process technical review (your existing review logic)
        review_result = {
            'status': 'REVIEWED',
            'technical_complexity': 'MEDIUM',
            'implementation_notes': [
                'Consider using AWS Cognito for auth',
                'Implement rate limiting',
                'Add email verification'
            ],
            'security_considerations': [
                'Password complexity requirements',
                'Token expiration',
                'Rate limiting'
            ],
            'estimated_effort': 'MEDIUM'
        }
        
        # Store review results
        review_item = {
            'story_id': story_id,
            'version': 'TECH_REVIEW',
            'content': review_result,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Update DynamoDB
        table.put_item(Item=review_item)
        
        # Return result to Step Functions
        if task_token:
            sfn = boto3.client('stepfunctions')
            sfn.send_task_success(
                taskToken=task_token,
                output=json.dumps({
                    'story_id': story_id,
                    'status': 'REVIEWED',
                    'review': review_result
                })
            )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'story_id': story_id,
                'message': 'Technical review completed',
                'status': 'COMPLETED',
                'review': review_result
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
                error='TechnicalReviewWorkerError',
                cause=str(e)
            )
        
        return {
            'statusCode': 500,
            'body': json.dumps(error_response)
        } 