"""
analyze_story_worker Lambda Function

This Lambda processes stories and creates the AGILE_COACH version with analysis.
It's triggered by Step Functions.

Environment Variables:
    DYNAMODB_TABLE (str): Name of the DynamoDB table for storing stories
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
    """Analyzes the user story (stubbed for testing).
    Returns both original content and analysis for testing purposes."""
    return {
        # Keep original story content for testing
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
        
        # Get the PENDING version from DynamoDB using composite key
        response = table.get_item(
            Key={
                'story_id': story_id,
                'version': 'AGILE_COACH_PENDING'  # This is the composite key
            }
        )
        
        if 'Item' not in response:
            raise ValueError(f"No PENDING story found for story_id: {story_id}")
            
        item = response['Item']
        
        # Extract data
        content = item['content']
        tenant_id = item['tenant_id']
        
        # Analyze the story (will be OpenAI later)
        analysis_results = analyze_story(content)
        
        # Store analyzed version (just the analysis results)
        timestamp = datetime.utcnow().isoformat()
        analyzed_item = {
            'story_id': story_id,
            'version': 'AGILE_COACH',  # This version for the analyzed content
            'tenant_id': tenant_id,
            'content': analysis_results,  # Store just the AI analysis
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        logger.info(f"Storing analyzed item in DynamoDB: {json.dumps(analyzed_item)}")
        table.put_item(Item=analyzed_item)
        
        return {
            'story_id': story_id,
           
        }
        
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}", exc_info=True)
        raise

