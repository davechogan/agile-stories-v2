import json
import boto3
import os
import logging
from datetime import datetime, UTC

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
sfn = boto3.client('stepfunctions')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    """
    Handles workflow signals from UI actions.
    
    Expected event format:
    {
        "pathParameters": {
            "storyId": "uuid",
            "action": "action-name"
        }
    }
    """
    try:
        logger.info(f"Processing workflow signal: {json.dumps(event)}")
        
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
                ':time': datetime.now(UTC).isoformat()
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

def handler(event, context):
    """
    Handler for workflow signal events
    """
    logger.info(f"Received event: {json.dumps(event, indent=2)}")
    
    try:
        # Parse Step Functions input
        if isinstance(event.get('input'), str):
            parsed_event = json.loads(event['input'])
        else:
            parsed_event = event
            
        action = parsed_event.get('action')
        story_id = parsed_event.get('story_id')
        token = parsed_event.get('token')
        
        logger.info(f"Parsed event - action: {action}, story_id: {story_id}, token: {token}")
        
        if action == 'NAVIGATE_TO_AGILE':
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'action': 'NAVIGATE',
                    'path': '/agile'
                })
            }
            
        elif action == 'WAIT_FOR_TECH_REVIEW_DECISION':
            task_token = parsed_event.get('taskToken')
            table.update_item(
                Key={'story_id': story_id},
                UpdateExpression='SET task_token = :token',
                ExpressionAttributeValues={
                    ':token': task_token
                }
            )
            return {
                'statusCode': 200,
                'message': 'Waiting for tech review decision'
            }
            
        else:
            raise ValueError(f"Unknown action: {action}")
            
    except Exception as e:
        logger.error(f"Error in workflow_signal_handler: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'error': str(e)
        }

def get_active_connections(token):
    """Get active WebSocket connections for a token"""
    # TODO: Implement actual connection lookup
    logger.info(f"Getting active connections for token: {token}")
    return ['dummy-connection-id']  # Replace with actual implementation

def send_websocket_message(connection_id, message):
    """Send message to WebSocket connection"""
    logger.info(f"Sending to connection {connection_id}: {json.dumps(message)}")
    # TODO: Implement actual WebSocket send
    # Use AWS API Gateway Management API to send the message 