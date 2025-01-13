"""
Story Analysis Lambda Handler

This module handles the initial submission of user stories for analysis.
It stores the original story in DynamoDB and queues it for AI analysis.

Flow:
1. Receives story from API Gateway
2. Generates UUID for the story
3. Stores original story in DynamoDB
4. Queues story for AI analysis via SQS
5. Returns story ID to client

Environment Variables:
    DYNAMODB_TABLE: Name of the DynamoDB table
    ANALYSIS_QUEUE_URL: URL of the SQS queue for analysis

Returns:
    API Gateway response with story ID or error
"""

import json
import os
import uuid
from datetime import datetime
import boto3

dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
queue_url = os.environ['ANALYSIS_QUEUE_URL']

def handler(event, context):
    try:
        # Parse input
        body = json.loads(event['body'])
        story_id = str(uuid.uuid4())
        
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
        
        # Send to SQS for analysis
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps({
                'story_id': story_id
            })
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'story_id': story_id,
                'message': 'Story submitted for analysis'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 