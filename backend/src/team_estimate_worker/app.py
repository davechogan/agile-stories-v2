"""
Team Estimate Worker Lambda Function

This Lambda:
1. Receives a role and story payload
2. Gets OpenAI analysis for estimation
3. Returns formatted estimate
"""

import json
import openai
import boto3
import logging
from pathlib import Path

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
secrets_client = boto3.client('secretsmanager')

def get_openai_key():
    """Retrieve OpenAI API key from AWS Secrets Manager."""
    try:
        response = secrets_client.get_secret_value(
            SecretId="openai_key"
        )
        secrets = json.loads(response['SecretString'])
        openai.api_key = secrets['OPENAI_API_KEY']
    except Exception as e:
        logger.error(f"Failed to get OpenAI key: {str(e)}")
        raise

def get_role_prompt(role: str) -> str:
    """Load role-specific estimation prompt."""
    try:
        # Convert role to match file naming convention
        role_file = role.lower().replace(' ', '_')
        prompt_path = Path('/var/task') / f"{role_file}Prompt.md"
        
        with open(prompt_path, 'r') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Failed to read prompt for role {role}: {str(e)}")
        raise

def handler(event, context):
    try:
        # Get OpenAI key
        get_openai_key()
        
        # Log the incoming event for debugging
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Parse input - use content instead of story_data
        role = event['role']
        content = event['content']  # This matches what team_estimate sends
        
        logger.info(f"Processing estimation for role: {role}")
        logger.info(f"Content: {json.dumps(content)}")

        # Get role-specific prompt
        prompt = get_role_prompt(role)

        # Get OpenAI estimation
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": json.dumps(content)}
            ],
            response_format={ "type": "json_object" }
        )
        
        # Parse and return response
        estimate = json.loads(response.choices[0].message.content)
        logger.info(f"Estimation result: {json.dumps(estimate)}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(estimate)
        }
        
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }