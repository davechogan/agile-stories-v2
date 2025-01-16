"""
Story Analysis Worker Lambda

This module performs the AI analysis of user stories.
It processes stories from Step Functions and updates results in DynamoDB.

Flow:
1. Receives story from Step Functions task
2. Performs AI analysis
3. Stores analysis results in DynamoDB
4. Returns analysis status to Step Functions
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
        # Get task token if exists
        task_token = event.get('taskToken')
        
        # Get story details
        story_id = event['story_id']
        title = event['title']
        description = event['description']
        acceptance_criteria = event['acceptance_criteria']
        
        # Perform analysis (your existing analysis logic)
        analysis_result = {
            'status': 'AGILE_COACH',
            'analysis': 'AI analysis results here',
            'suggestions': [
                'Suggestion 1',
                'Suggestion 2'
            ],
            'complexity_score': 3
        }
        
        # Store analysis results
        analysis_item = {
            'story_id': story_id,
            'version': 'ANALYSIS',
            'content': analysis_result,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Update DynamoDB
        table.put_item(Item=analysis_item)
        
        # Return result to Step Functions
        if task_token:
            sfn = boto3.client('stepfunctions')
            sfn.send_task_success(
                taskToken=task_token,
                output=json.dumps({
                    'story_id': story_id,
                    'status': 'AGILE_COACH',
                    'analysis': analysis_result
                })
            )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'story_id': story_id,
                'message': 'Analysis completed',
                'status': 'COMPLETED',
                'analysis': analysis_result
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
                error='AnalysisWorkerError',
                cause=str(e)
            )
        
        return {
            'statusCode': 500,
            'body': json.dumps(error_response)
        } 