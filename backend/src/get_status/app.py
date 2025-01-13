import json
import os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def handler(event, context):
    try:
        story_id = event['pathParameters']['id']
        
        # Query all versions for this story
        response = table.query(
            KeyConditionExpression=Key('story_id').eq(story_id)
        )
        
        # Map versions to status
        versions = [item['version'] for item in response['Items']]
        
        status = {
            'story_id': story_id,
            'status': 'IN_PROGRESS',
            'steps': {
                'original': 'ORIGINAL' in versions,
                'agile_coach': 'AGILE_COACH' in versions,
                'senior_dev': 'SENIOR_DEV' in versions,
                'team_estimates': any(v.startswith('TEAM_ESTIMATES#') for v in versions),
                'final': 'FINAL' in versions
            },
            'current_step': 'PENDING'
        }
        
        # Determine current step
        if 'FINAL' in versions:
            status['status'] = 'COMPLETED'
            status['current_step'] = 'COMPLETED'
        elif any(v.startswith('TEAM_ESTIMATES#') for v in versions):
            status['current_step'] = 'TEAM_ESTIMATES'
        elif 'SENIOR_DEV' in versions:
            status['current_step'] = 'TEAM_ESTIMATES_PENDING'
        elif 'AGILE_COACH' in versions:
            status['current_step'] = 'SENIOR_DEV_PENDING'
        elif 'ORIGINAL' in versions:
            status['current_step'] = 'AGILE_COACH_PENDING'
        
        return {
            'statusCode': 200,
            'body': json.dumps(status)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 