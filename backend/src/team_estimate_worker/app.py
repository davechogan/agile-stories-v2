"""
team_estimate_worker Lambda Function

This Lambda is invoked in parallel by the team_estimate Lambda to generate
role-specific estimates for a story. It:
1. Loads role-specific prompt
2. Generates estimates using OpenAI
3. Stores results in DynamoDB
4. Returns formatted estimate data to the main Lambda

Environment Variables:
    ESTIMATES_TABLE (str): Name of the DynamoDB table for storing estimates
    OPENAI_API_KEY (str): OpenAI API key for generating estimates
"""

import os
import json
import boto3
import logging
from datetime import datetime
from pathlib import Path
from .test_data import get_test_estimate

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
estimates_table = dynamodb.Table(os.environ['ESTIMATES_TABLE'])

def load_role_prompt(role: str) -> str:
    """
    Loads the prompt template for the specified role.
    
    Args:
        role (str): The role ID (e.g., 'senior_dev', 'qa_engineer')
        
    Returns:
        str: The prompt template for the role
    """
    try:
        prompt_path = Path(__file__).parent / 'prompts' / f'{role}Prompt.md'
        with open(prompt_path, 'r') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading prompt for role {role}: {str(e)}")
        # Fallback to basic prompt if role-specific one not found
        return """Please estimate this story from your role's perspective.
                 Provide story points, person days, and detailed justification."""

def generate_estimate(role: str, story_data: dict) -> dict:
    """
    Generates an estimate for a specific role (using test data for now).
    """
    # TODO: Replace with OpenAI integration later
    return get_test_estimate(role)

def store_estimate(story_id: str, role: str, estimate_data: dict, tenant_id: str):
    """
    Stores the estimate in DynamoDB.
    
    Args:
        story_id (str): The story's UUID
        role (str): The estimating role
        estimate_data (dict): The estimate details
        tenant_id (str): The tenant ID
    """
    try:
        timestamp = datetime.utcnow().isoformat()
        estimation_id = f"{story_id}_{role}"
        
        item = {
            'estimation_id': estimation_id,
            'story_id': story_id,
            'tenantId': tenant_id,
            'role': role,
            'estimates': estimate_data['estimates'],
            'justification': estimate_data['justification'],
            'created_at': timestamp
        }
        
        estimates_table.put_item(Item=item)
        
    except Exception as e:
        logger.error(f"Error storing estimate: {str(e)}")
        raise

def handler(event, context):
    """
    Lambda handler for generating role-specific estimates.
    
    Args:
        event (dict): Event containing:
            role (str): Role to generate estimate for
            story_data (dict): Story content and context
            story_id (str): Story UUID
            tenant_id (str): Tenant ID
            
    Returns:
        dict: Generated estimate data
    """
    try:
        logger.info(f"Processing estimate request: {json.dumps(event)}")
        
        role = event['role']
        story_data = event['story_data']
        story_id = story_data['story_id']
        tenant_id = story_data['tenant_id']
        
        # Generate estimate
        estimate_data = generate_estimate(role, story_data)
        
        # Store in DynamoDB
        store_estimate(story_id, role, estimate_data, tenant_id)
        
        # Return estimate data for aggregation
        return {
            'statusCode': 200,
            'body': {
                'role': role,
                'estimates': estimate_data['estimates'],
                'justification': estimate_data['justification']
            }
        }
        
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': {
                'error': str(e)
            }
        } 