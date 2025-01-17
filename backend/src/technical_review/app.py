"""
technical_review Lambda Function

TEMPORARY TEST MODE:
This Lambda is normally triggered by API Gatewaythe user input sent to the step function workflow when a user submits the story for technical review.
However, for testing the workflow, it currently:
1. Gets the AGILE_COACH version from DynamoDB using the story_id
2. Creates a SENIOR_DEV_PENDING version
3. Passes the story_id to the worker

In production, it will:
1. Receive the user's edited story via THE STEP FUNCTIONS WORKFLOW
2. Create SENIOR_DEV_PENDING version with user edits
3. Start the technical review workflow
"""

import os
import json
import boto3
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def handler(event, context):
    """Lambda handler for processing technical review requests."""
    try:
        logger.info(f"Event received: {json.dumps(event)}")
        
        # Get story_id from Step Functions
        story_id = event['story_id']
        
        # Get AGILE_COACH version
        response = table.get_item(
            Key={
                'story_id': story_id,
                'version': 'AGILE_COACH'
            }
        )
        
        if 'Item' not in response:
            raise ValueError(f"No AGILE_COACH version found for story_id: {story_id}")
            
        agile_coach_version = response['Item']
        tenant_id = agile_coach_version['tenant_id']  # Get tenant_id from the story
        
        # Create SENIOR_DEV_PENDING version
        timestamp = datetime.utcnow().isoformat()
        pending_item = {
            'story_id': story_id,
            'version': 'SENIOR_DEV_PENDING',
            'tenant_id': tenant_id,  # Use tenant_id from the story
            'content': agile_coach_version['content'],
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        logger.info(f"Storing SENIOR_DEV_PENDING version for story_id: {story_id}")
        table.put_item(Item=pending_item)
        
        return {
            'story_id': story_id
        }
        
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}", exc_info=True)
        raise 