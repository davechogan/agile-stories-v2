"""
Technical Review Lambda Handler

This Lambda initiates the technical review of a story that has been analyzed by the Agile Coach.
It queues the story for senior developer analysis.

Flow:
1. Receives story_id from API
2. Verifies AGILE_COACH version exists
3. Queues for senior dev review
4. Returns status to client

Environment Variables:
    DYNAMODB_TABLE: DynamoDB table name
    TECHNICAL_REVIEW_QUEUE_URL: SQS queue URL for technical review
"""

import json
import os
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def handler(event, context):
    try:
        # Parse input
        body = json.loads(event['body'])
        story_id = body['story_id']
        
        # Verify AGILE_COACH version exists
        try:
            response = table.get_item(
                Key={
                    'story_id': story_id,
                    'version': 'AGILE_COACH'
                }
            )
            if 'Item' not in response:
                return {
                    'statusCode': 404,
                    'body': json.dumps({
                        'error': 'Story not found or Agile Coach analysis not completed'
                    })
                }
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': f"Database error: {str(e)}"
                })
            }
        
        # Queue for technical review
        try:
            sqs.send_message(
                QueueUrl=os.environ['TECHNICAL_REVIEW_QUEUE_URL'],
                MessageBody=json.dumps({
                    'story_id': story_id
                })
            )
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': f"Queue error: {str(e)}"
                })
            }
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'story_id': story_id,
                'message': 'Story queued for technical review'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 