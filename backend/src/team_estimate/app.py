"""
Team Estimation Lambda Handler

This Lambda initiates the team estimation process for a story that has been technically reviewed.
It queues the story for estimation by each team member's AI agent.

Flow:
1. Receives story_id from API
2. Verifies SENIOR_DEV version exists
3. Queues for each team member's estimation
4. Returns status to client

Environment Variables:
    DYNAMODB_TABLE: DynamoDB table name
    ESTIMATION_QUEUE_URL: SQS queue URL for team estimation
    TEAM_MEMBERS: JSON string of team members array [{"id": "string", "role": "string"}]
"""

import json
import os
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def get_team_members():
    """Get team members from environment variable"""
    return json.loads(os.environ['TEAM_MEMBERS'])

def handler(event, context):
    try:
        # Parse input
        body = json.loads(event['body'])
        story_id = body['story_id']
        
        # Verify SENIOR_DEV version exists
        try:
            response = table.get_item(
                Key={
                    'story_id': story_id,
                    'version': 'SENIOR_DEV'
                }
            )
            if 'Item' not in response:
                return {
                    'statusCode': 404,
                    'body': json.dumps({
                        'error': 'Story not found or technical review not completed'
                    })
                }
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': f"Database error: {str(e)}"
                })
            }
        
        # Queue estimation tasks for each team member
        team_members = get_team_members()
        queued_members = []
        
        for member in team_members:
            try:
                sqs.send_message(
                    QueueUrl=os.environ['ESTIMATION_QUEUE_URL'],
                    MessageBody=json.dumps({
                        'story_id': story_id,
                        'member_id': member['id'],
                        'role': member['role']
                    })
                )
                queued_members.append(member['id'])
            except ClientError as e:
                return {
                    'statusCode': 500,
                    'body': json.dumps({
                        'error': f"Queue error for member {member['id']}: {str(e)}"
                    })
                }
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'story_id': story_id,
                'message': 'Story queued for team estimation',
                'queued_members': queued_members
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 