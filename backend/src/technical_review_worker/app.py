"""
technical_review_worker Lambda Function

This Lambda is triggered by Step Functions to perform technical review analysis on a story.
It creates a SENIOR_DEV version with technical review results in DynamoDB.

Environment Variables:
    DYNAMODB_TABLE (str): Name of the DynamoDB table for storing stories
    OPENAI_API_KEY (str): OpenAI API key for technical analysis

Returns:
    dict: Step Functions response object containing:
        story_id (str): UUID of the processed story
        tenant_id (str): Tenant identifier
        technical_review (dict): Technical review results
        content (dict): Story content
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

def perform_technical_review(content):
    """
    Analyzes the story from a technical perspective using AI.
    
    Args:
        content (dict): Story content containing:
            title (str): Story title
            description (str): Story description
            story (str): User story
            acceptance_criteria (list): List of acceptance criteria
            analysis (dict): Previous agile coach analysis
    
    Returns:
        dict: Technical review results containing:
            technical_considerations (list): List of technical points
            complexity_score (int): Complexity rating (1-10)
            estimated_effort (str): Estimated effort level
    
    Note:
        This is currently a placeholder. Actual implementation will use OpenAI.
    """
    return {
        "technical_considerations": [
            "Consider adding API rate limiting",
            "Need to handle offline scenarios"
        ],
        "complexity_score": 7,
        "estimated_effort": "medium"
    }

def handler(event, context):
    """
    Lambda handler for processing technical review requests.
    
    Performs technical analysis of the story and creates a SENIOR_DEV
    version with the results.
    
    Args:
        event (dict): Step Functions event object containing:
            story_id (str): UUID of the story
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
        
        # Perform technical review
        tech_review_results = perform_technical_review(content)
        
        # Store technical review results as new version
        complete_item = {
            'story_id': story_id,
            'version': 'SENIOR_DEV',
            'tenant_id': tenant_id,
            'content': {
                **content,  # Previous content
                'technical_review': tech_review_results
            },
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        logger.info(f"Storing SENIOR_DEV version in DynamoDB: {json.dumps(complete_item)}")
        table.put_item(Item=complete_item)
        
        # Return results to Step Functions
        return {
            'story_id': story_id,
            'tenant_id': tenant_id,
            'technical_review': tech_review_results,
            'content': content
        }
        
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}", exc_info=True)
        raise 