"""
team_estimate_worker Lambda Function

This Lambda is triggered by Step Functions to generate team estimates for a story.
It creates a FINAL version with estimation results in DynamoDB.

Environment Variables:
    DYNAMODB_TABLE (str): Name of the DynamoDB table for storing stories
    ESTIMATES_TABLE (str): Name of the DynamoDB table for storing individual estimates
    OPENAI_API_KEY (str): OpenAI API key for estimation analysis

Returns:
    dict: Step Functions response object containing:
        story_id (str): UUID of the processed story
        tenant_id (str): Tenant identifier
        estimates (dict): Aggregated estimation results
        content (dict): Story content
"""

import os
import json
import boto3
import logging
from datetime import datetime
from statistics import mean

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')

# Get DynamoDB tables
stories_table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
estimates_table = dynamodb.Table(os.environ['ESTIMATES_TABLE'])

def generate_team_member_estimate(content, role):
    """
    Generates an estimate for a single team member/role using AI.
    
    Args:
        content (dict): Story content containing:
            title (str): Story title
            description (str): Story description
            story (str): User story
            acceptance_criteria (list): List of acceptance criteria
            technical_review (dict): Technical review results
        role (str): Team member role (e.g., 'frontend', 'backend')
    
    Returns:
        dict: Individual estimate containing:
            points (int): Story points estimate
            days (float): Days estimate
            justification (str): Reasoning for the estimate
    
    Note:
        This is currently a placeholder. Actual implementation will use OpenAI.
    """
    return {
        "points": 5,
        "days": 3.5,
        "justification": f"Based on {role} complexity and technical requirements"
    }

def store_individual_estimate(story_id, tenant_id, role, estimate):
    """
    Stores an individual team member's estimate in the estimates table.
    
    Args:
        story_id (str): UUID of the story
        tenant_id (str): Tenant identifier
        role (str): Team member role
        estimate (dict): Individual estimate results
    """
    timestamp = datetime.utcnow().isoformat()
    
    item = {
        'story_id': story_id,
        'team_member_id': f"{role}-{timestamp}",  # Using role+timestamp as unique ID
        'tenant_id': tenant_id,
        'role': role,
        'estimate_points': estimate['points'],
        'estimate_days': estimate['days'],
        'justification': estimate['justification'],
        'created_at': timestamp
    }
    
    estimates_table.put_item(Item=item)

def aggregate_estimates(estimates):
    """
    Aggregates individual estimates into team consensus.
    
    Args:
        estimates (list): List of individual estimates
    
    Returns:
        dict: Aggregated results containing:
            average_points (float): Mean of story points
            average_days (float): Mean of day estimates
            point_range (tuple): Min and max points
            day_range (tuple): Min and max days
    """
    points = [e['points'] for e in estimates]
    days = [e['days'] for e in estimates]
    
    return {
        'average_points': mean(points),
        'average_days': mean(days),
        'point_range': (min(points), max(points)),
        'day_range': (min(days), max(days))
    }

def handler(event, context):
    """
    Lambda handler for processing team estimation requests.
    
    Generates estimates from multiple team members and creates a FINAL
    version with aggregated results.
    
    Args:
        event (dict): Step Functions event object containing:
            story_id (str): UUID of the story
            tenant_id (str): Tenant identifier
            content (dict): Story content to estimate
            team_config (dict): Team configuration settings
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
        team_config = event.get('team_config', {
            'roles': ['frontend', 'backend', 'qa']  # Default roles if not specified
        })
        timestamp = datetime.utcnow().isoformat()
        
        # Generate individual estimates
        individual_estimates = []
        for role in team_config['roles']:
            estimate = generate_team_member_estimate(content, role)
            store_individual_estimate(story_id, tenant_id, role, estimate)
            individual_estimates.append(estimate)
        
        # Aggregate estimates
        aggregated_results = aggregate_estimates(individual_estimates)
        
        # Store final results
        final_item = {
            'story_id': story_id,
            'version': 'FINAL',
            'tenant_id': tenant_id,
            'content': {
                **content,
                'team_estimates': {
                    'individual_estimates': individual_estimates,
                    'aggregated_results': aggregated_results
                }
            },
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        logger.info(f"Storing FINAL version in DynamoDB: {json.dumps(final_item)}")
        stories_table.put_item(Item=final_item)
        
        # Return results to Step Functions
        return {
            'story_id': story_id,
            'tenant_id': tenant_id,
            'estimates': {
                'individual_estimates': individual_estimates,
                'aggregated_results': aggregated_results
            },
            'content': content
        }
        
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}", exc_info=True)
        raise 