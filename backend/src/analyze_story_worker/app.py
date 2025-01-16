"""
analyze_story_worker Lambda Function

This Lambda is triggered by Step Functions to perform AI analysis on a submitted story.
It creates an AGILE_COACH version with analysis results in DynamoDB.

Environment Variables:
    DYNAMODB_TABLE (str): Name of the DynamoDB table for storing stories
    OPENAI_API_KEY (str): OpenAI API key for story analysis
    
Returns:
    dict: Step Functions response object containing:
        story_id (str): UUID of the processed story
        tenant_id (str): Tenant identifier
        analysis (dict): Analysis results from AI
        content (dict): Original story content
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

# Get DynamoDB table
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def analyze_story(content):
    """
    Analyzes the user story using AI to provide suggestions and improvements.
    
    Args:
        content (dict): Story content containing:
            title (str): Story title
            description (str): Story description
            story (str): User story
            acceptance_criteria (list): List of acceptance criteria
    
    Returns:
        dict: Analysis results containing:
            suggestions (list): List of improvement suggestions
            score (int): Story quality score (0-100)
    
    Note:
        This is currently a placeholder. Actual implementation will use OpenAI.
    """
    # Placeholder for actual analysis
    return {
        "suggestions": [
            "Consider adding more specific acceptance criteria",
            "The story description could be more detailed"
        ],
        "score": 85
    }

def handler(event, context):
    """
    Lambda handler for processing story analysis requests.
    
    Creates a PENDING version first, then performs AI analysis and creates
    an AGILE_COACH version with the results.
    
    Args:
        event (dict): Step Functions event object containing:
            story_id (str): UUID of the story to analyze
            tenant_id (str): Tenant identifier
            content (dict): Story content to analyze
        context (obj): Lambda context object
    
    Returns:
        dict: Step Functions response object
    
    Raises:
        Exception: For any processing errors
    """
    try:
        logger.info(f"Event received: {json.dumps(event)}")
        
        # Extract data from Step Functions input
        story_id = event['story_id']
        tenant_id = event.get('tenant_id', 'default')
        content = event['content']
        timestamp = datetime.utcnow().isoformat()
        
        # First, create PENDING version
        pending_item = {
            'story_id': story_id,
            'version': 'AGILE_COACH_PENDING',
            'tenant_id': tenant_id,
            'content': content,  # Original content
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        logger.info(f"Storing PENDING version in DynamoDB: {json.dumps(pending_item)}")
        table.put_item(Item=pending_item)
        
        # Perform analysis
        analysis_results = analyze_story(content)
        
        # Store analysis results as new version
        complete_item = {
            'story_id': story_id,
            'version': 'AGILE_COACH',
            'tenant_id': tenant_id,
            'content': {
                **content,  # Original story content
                'analysis': analysis_results
            },
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        logger.info(f"Storing AGILE_COACH version in DynamoDB: {json.dumps(complete_item)}")
        table.put_item(Item=complete_item)
        
        # Return results to Step Functions
        return {
            'story_id': story_id,
            'tenant_id': tenant_id,
            'analysis': analysis_results,
            'content': content
        }
        
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}", exc_info=True)
        raise 