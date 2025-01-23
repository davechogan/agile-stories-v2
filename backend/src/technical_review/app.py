"""
Technical Review Lambda Function

This Lambda handles the technical review process:
1. Saves the current story state as SENIOR_DEV_PENDING
2. Gets OpenAI analysis with senior dev role
3. Saves the analysis as SENIOR_DEV

Environment Variables:
    DYNAMODB_TABLE (str): Name of the DynamoDB table
    OPENAI_API_KEY (str): OpenAI API key
"""

import os
import json
import boto3
from datetime import datetime, UTC
import openai
from pathlib import Path

# Initialize AWS clients
secrets_client = boto3.client('secretsmanager')

def get_technical_prompt():
    """Load technical review prompt template."""
    try:
        # First try to read from file
        prompt_path = Path(__file__).parent / "SeniorDevPrompt.md"
        
        with open(prompt_path, 'r') as f:
            return f.read()
            
    except Exception as e:
        print(f"Failed to read senior dev prompt: {str(e)}")
        # Fallback to hardcoded prompt
        return """
You are a Senior Software Developer with over 15 years of experience in software architecture, design patterns, and best practices. Your expertise spans multiple programming languages, frameworks, and technology stacks. Your role is to review user stories from a technical implementation perspective.

Your analysis should focus on:
1. Technical feasibility and complexity
2. Potential architectural impacts
3. Dependencies and integration points
4. Security considerations
5. Performance implications
6. Testing requirements

Please analyze the provided user story and provide feedback in the following JSON format:
{
    "technical_score": "1-10 rating of technical clarity and feasibility",
    "implementation_concerns": ["List of technical concerns"],
    "architecture_impact": ["Potential impacts on system architecture"],
    "dependencies": ["Required system dependencies"],
    "testing_requirements": ["Key testing considerations"],
    "technical_suggestions": ["Specific technical recommendations"]
}
"""

def get_openai_key():
    """Retrieve OpenAI API key from AWS Secrets Manager."""
    try:
        response = secrets_client.get_secret_value(
            SecretId="openai_key"
        )
        secrets = json.loads(response['SecretString'])
        api_key = secrets['OPENAI_API_KEY']
        
        # Set the key for the OpenAI client
        openai.api_key = api_key
        
        return api_key
    except Exception as e:
        print(f"Failed to get OpenAI key: {str(e)}")
        raise

def handler(event, context):
    try:
        # Get and set OpenAI key first, before making any OpenAI calls
        get_openai_key()
        
        # Parse request
        body = json.loads(event.get('body', '{}'))
        story_id = body.get('story_id')
        tenant_id = body.get('tenant_id')
        improved_content = body.get('analysis', {}).get('content', {})
        
        current_time = datetime.now(UTC).isoformat().replace('+00:00', 'Z')
        
        # Initialize DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE', 'dev-agile-stories'))
        
        # Save improved content from AGILE_COACH in PENDING
        pending_item = {
            'story_id': story_id,
            'version': 'SENIOR_DEV_PENDING',
            'tenant_id': tenant_id,
            'created_at': current_time,
            'updated_at': current_time,
            'content': {  # Improved content from AGILE_COACH
                'title': improved_content.get('title', ''),
                'story': improved_content.get('story', ''),
                'description': '',
                'acceptance_criteria': improved_content.get('acceptance_criteria', [])
            },
            'analysis': {  # Empty until agent responds
                'content': {},
                'analysis': {}
            }
        }
        
        table.put_item(Item=pending_item)
        
        # Get SENIOR_DEV analysis using improved content
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": get_technical_prompt()},
                {"role": "user", "content": json.dumps(pending_item['content'])}
            ],
            response_format={ "type": "json_object" }
        )
        
        # Parse and store final response
        analysis = json.loads(response.choices[0].message.content)
        
        final_item = {
            'story_id': story_id,
            'version': 'SENIOR_DEV',
            'tenant_id': tenant_id,
            'created_at': current_time,
            'updated_at': current_time,
            'content': pending_item['content'],  # Keep improved content
            'analysis': analysis  # Agent's response with technical details
        }
        
        table.put_item(Item=final_item)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'story_id': story_id,
                'version': 'SENIOR_DEV',
                'analysis': analysis
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 