import json
import boto3
import os
import logging
from datetime import datetime, UTC

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    """
    Handles state transitions and stores task tokens.
    
    Expected event format:
    {
        "story_id": "uuid",
        "status": "STATE_NAME",
        "taskToken": "step-functions-task-token"
    }
    """
    try:
        logger.info(f"Processing state transition: {json.dumps(event)}")
        
        story_id = event['story_id']
        status = event['status']
        task_token = event['taskToken']
        
        # Update DynamoDB with new state and token
        table.update_item(
            Key={
                'story_id': story_id,
                'version': status
            },
            UpdateExpression='SET task_token = :token, updated_at = :time',
            ExpressionAttributeValues={
                ':token': task_token,
                ':time': datetime.now(UTC).isoformat()
            }
        )
        
        logger.info(f"Successfully stored token for story {story_id}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'State transition processed',
                'story_id': story_id,
                'status': status
            })
        }
        
    except Exception as e:
        logger.error(f"Error processing state transition: {str(e)}", exc_info=True)
        raise 