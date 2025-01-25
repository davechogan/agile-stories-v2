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

import json
import os
import boto3
import logging
from datetime import datetime
from typing import Dict, Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
estimates_table = dynamodb.Table(os.environ.get('ESTIMATES_TABLE', 'dev-agile-stories-estimations'))

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

def generate_role_estimate(role: str, content: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate estimates based on role and story content.
    
    Args:
        role (str): The role (Frontend, Backend, Database)
        content (dict): Story content including implementation details
        
    Returns:
        dict: Estimate object with story points and person days
    """
    # Get implementation details for this role
    implementation_details = content.get('implementation_details', [])
    role_details = [d for d in implementation_details if d.get('type') == role]
    
    # Base estimates
    story_points = 3  # Default medium complexity
    person_days = 2   # Default 2 days
    confidence = 'MEDIUM'
    
    # Adjust based on number of tasks
    num_tasks = len(role_details)
    if num_tasks > 5:
        story_points += 2
        person_days += 2
        confidence = 'LOW'
    elif num_tasks > 3:
        story_points += 1
        person_days += 1
    elif num_tasks < 2:
        confidence = 'HIGH'
    
    # Generate justification
    task_list = "\n".join([f"- {d.get('text')}" for d in role_details])
    justification = f"""
Role: {role}
Number of tasks: {num_tasks}

Tasks:
{task_list}

Estimate based on:
- Task complexity and quantity
- Implementation details specific to {role}
- Standard velocity metrics
"""
    
    return {
        'estimates': {
            'story_points': {
                'value': story_points,
                'confidence': confidence
            },
            'person_days': {
                'value': person_days,
                'confidence': confidence
            }
        },
        'justification': justification.strip()
    }

def handler(event, context):
    """
    Process estimation request for a specific role.
    
    Expected event structure:
    {
        'story_id': 'story123',
        'tenant_id': 'tenant123',
        'role': 'Frontend',
        'content': { story content with implementation_details }
    }
    """
    try:
        logger.info(f"Processing estimate request: {json.dumps(event)}")
        
        # Extract data from event
        story_id = event['story_id']
        tenant_id = event['tenant_id']
        role = event['role']
        content = event['content']
        
        # Generate role-specific estimate
        estimate_result = generate_role_estimate(role, content)
        
        # Create complete estimate record
        estimate_record = {
            'estimation_id': f"{story_id}_{role}",
            'story_id': story_id,
            'tenantId': tenant_id,
            'created_at': datetime.utcnow().isoformat(),
            'role': role,
            **estimate_result  # Includes estimates and justification
        }
        
        # Save to DynamoDB
        logger.info(f"Saving estimate for {role}: {json.dumps(estimate_record)}")
        estimates_table.put_item(Item=estimate_record)
        
        return {
            'statusCode': 200,
            'body': json.dumps(estimate_record)
        }
        
    except Exception as e:
        logger.error(f"Error processing {event.get('role')} estimate: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 