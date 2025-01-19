import json
import boto3
import os
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

sfn = boto3.client('stepfunctions')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    """Generic handler for workflow signals from UI actions."""
    try:
        story_id = event['pathParameters']['storyId']
        action = event['pathParameters']['action']
        
        # Get story data including token from DynamoDB
        story_data = table.get_item(
            Key={'story_id': story_id}
        )['Item']
        
        task_token = story_data.get('task_token')
        if not task_token:
            raise ValueError(f"No task token found for story {story_id}")
            
        # Map actions to next states
        next_states = {
            'agile-review': 'TECH_REVIEW_PENDING',
            'tech-review': 'ESTIMATION_PENDING',
            'estimation': 'COMPLETE'
        }
        
        next_state = next_states.get(action)
        if not next_state:
            raise ValueError(f"Invalid action: {action}")
            
        # Signal state machine to continue
        sfn.send_task_success(
            taskToken=task_token,
            output=json.dumps({
                'story_id': story_id,
                'status': next_state
            })
        )
        
        # Update story status in DynamoDB
        table.update_item(
            Key={'story_id': story_id},
            UpdateExpression='SET #status = :status, last_updated = :time',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': next_state,
                ':time': datetime.utcnow().isoformat()
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully processed {action}',
                'story_id': story_id,
                'status': next_state
            })
        }
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 