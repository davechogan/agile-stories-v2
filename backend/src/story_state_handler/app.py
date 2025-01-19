import json
import boto3
import os
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    """Handles story state changes and stores task tokens."""
    try:
        # Extract data from Step Functions input
        story_id = event['story_id']
        status = event.get('status', 'PENDING')
        task_token = event.get('taskToken')  # Step Functions provides this
        
        # Update story in DynamoDB with new status and token
        update_expr = 'SET #status = :status, last_updated = :time'
        expr_attrs = {
            '#status': 'status',
            ':status': status,
            ':time': datetime.utcnow().isoformat()
        }
        
        # Only include token if provided
        if task_token:
            update_expr += ', task_token = :token'
            expr_attrs[':token'] = task_token
        
        table.update_item(
            Key={'story_id': story_id},
            UpdateExpression=update_expr,
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues=expr_attrs
        )
        
        return {
            'story_id': story_id,
            'status': status
        }
    except Exception as e:
        logger.error(f"Error updating story state: {str(e)}", exc_info=True)
        raise 