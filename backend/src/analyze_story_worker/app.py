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
from datetime import datetime, UTC

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
    """
    Handler for analyze_story_worker Lambda
    Creates mock analysis and signals when ready for navigation
    """
    try:
        logger.info(f"Received event: {json.dumps(event, indent=2)}")
        
        story_id = event.get('story_id')
        token = event.get('token')
        
        if not story_id or not token:
            raise ValueError("Missing required fields: story_id and token")
            
        # Get the PENDING version
        response = table.get_item(
            Key={
                'story_id': story_id,
                'version': 'AGILE_COACH_PENDING'
            }
        )
        
        if 'Item' not in response:
            raise ValueError(f"No pending story found for ID: {story_id}")
            
        pending_story = response['Item']
        
        # Create mock analysis results
        mock_analysis = {
            "analysis_results": {
                "acceptance_criteria": [
                    "User can submit a story through the form",
                    "Story is stored in DynamoDB",
                    "User is navigated to review page",
                    "Analysis results are displayed"
                ],
                "recommendations": [
                    "Consider adding input validation",
                    "Add error handling for database operations",
                    "Implement loading states for better UX"
                ],
                "story_points": 5,
                "complexity": "medium"
            }
        }
        
        # Store completed analysis as AGILE_COACH version
        table.put_item(
            Item={
                'story_id': story_id,
                'version': 'AGILE_COACH',
                'token': token,
                'content': pending_story.get('content', {}),
                'analysis': mock_analysis,
                'created_at': datetime.now(UTC).isoformat(),
                'updated_at': datetime.now(UTC).isoformat()
            }
        )
        
        # Return success with navigation signal
        return {
            'statusCode': 200,
            'body': {
                'story_id': story_id,
                'token': token,
                'action': 'NAVIGATE',
                'path': '/agile'
            }
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise

