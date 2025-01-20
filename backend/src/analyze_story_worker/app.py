"""
analyze_story_worker Lambda Function

This Lambda:
1. Gets AGILE_COACH_PENDING version from DynamoDB
2. Will send to OpenAI for analysis (currently mocked)
3. Stores results as AGILE_COACH version
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

def analyze_story(content):
    """
    Analyzes the user story (stubbed for testing).
    Returns both original content and analysis results.
    """
    return {
        # Keep original story content
        "title": content["title"],
        "description": content["description"],
        "story": content["story"],
        "acceptance_criteria": content["acceptance_criteria"],
        
        # Add analysis results
        "analysis": {
            "suggestions": ["Make acceptance criteria more specific"],
            "score": 85,
            "feedback": "Good story structure, could use more detailed acceptance criteria",
            "invest_analysis": {
                "independent": True,
                "negotiable": True,
                "valuable": True,
                "estimable": False,
                "small": True,
                "testable": True
            }
        }
    }

def handler(event, context):
    """Lambda handler for analyzing stories."""
    try:
        logger.info(f"Event received: {json.dumps(event)}")
        
        # Get story_id from event
        story_id = event['story_id']
        
        # Get the PENDING version from DynamoDB
        response = table.get_item(
            Key={
                'story_id': story_id,
                'version': 'AGILE_COACH_PENDING'
            }
        )
        
        if 'Item' not in response:
            raise ValueError(f"No PENDING story found for story_id: {story_id}")
            
        item = response['Item']
        content = item['content']
        tenant_id = item['tenant_id']
        token = item.get('token')  # Get token if it exists
        
        # Analyze the story and create new content
        analysis_results = analyze_story(content)
        
        # Store analyzed version
        timestamp = datetime.utcnow().isoformat()
        analyzed_item = {
            'story_id': story_id,
            'version': 'AGILE_COACH',
            'tenant_id': tenant_id,
            'token': token,  # Include token in analyzed version
            'content': analysis_results,
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        logger.info(f"Storing AGILE_COACH version in DynamoDB")
        table.put_item(Item=analyzed_item)
        
        return {
            'story_id': story_id,
            'token': token  # Return token for workflow
        }
        
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}", exc_info=True)
        raise

