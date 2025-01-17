"""
technical_review_worker Lambda Function

This Lambda:
1. Gets SENIOR_DEV_PENDING version from DynamoDB
2. Will send to OpenAI for technical analysis (currently mocked)
3. Stores results as SENIOR_DEV version
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

def analyze_technical_aspects(content):
    """
    TEMPORARY: Mock technical analysis that would come from OpenAI.
    Returns both original content and technical analysis.
    """
    return {
        # Keep original story content
        "title": content["title"],
        "description": content["description"],
        "story": content["story"],
        "acceptance_criteria": content["acceptance_criteria"],
        
        # Add technical analysis
        "technical_analysis": {
            "architecture_impact": "Minor - extends existing user management system",
            "security_considerations": [
                "Password hashing required",
                "Rate limiting for registration attempts",
                "Email verification tokens must be secure"
            ],
            "implementation_complexity": "Medium",
            "estimated_effort_days": 5,
            "technical_dependencies": [
                "User management service",
                "Email service",
                "Database migrations"
            ]
        }
    }

def handler(event, context):
    """Lambda handler for technical review analysis."""
    try:
        logger.info(f"Event received: {json.dumps(event)}")
        
        # Get story_id from Step Functions
        story_id = event['story_id']
        
        # Get SENIOR_DEV_PENDING version from DynamoDB
        response = table.get_item(
            Key={
                'story_id': story_id,
                'version': 'SENIOR_DEV_PENDING'
            }
        )
        
        if 'Item' not in response:
            raise ValueError(f"No SENIOR_DEV_PENDING version found for story_id: {story_id}")
            
        pending_item = response['Item']
        
        # Analyze technical aspects (mocked for now)
        analysis_results = analyze_technical_aspects(pending_item['content'])
        
        # Store SENIOR_DEV version
        timestamp = datetime.utcnow().isoformat()
        analyzed_item = {
            'story_id': story_id,
            'version': 'SENIOR_DEV',
            'tenant_id': pending_item['tenant_id'],
            'content': analysis_results,
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        logger.info(f"Storing SENIOR_DEV version: {json.dumps(analyzed_item)}")
        table.put_item(Item=analyzed_item)
        
        return {
            'story_id': story_id
        }
        
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}", exc_info=True)
        raise 