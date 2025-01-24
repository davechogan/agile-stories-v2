"""
analyze_story Lambda Function

This Lambda is triggered by API Gateway when a user submits a new story for analysis.
It creates the initial AGILE_COACH_PENDING version in DynamoDB and starts the Step Functions workflow.

Environment Variables:
    DYNAMODB_TABLE (str): Name of the DynamoDB table for storing stories
    ENVIRONMENT (str): Environment name (e.g., 'dev', 'prod')

Returns:
    dict: API Gateway response object
        statusCode (int): HTTP status code
        body (str): JSON string containing:
            story_id (str): UUID of the created story
            message (str): Success/error message
            status (str): Status of the operation
"""

import os
import sys
import json
import uuid
import boto3
import logging
import traceback
from datetime import datetime, UTC
from openai import OpenAI
from pathlib import Path
import requests

# Debug: Print Python path and current directory
print("Python Path:", sys.path)
print("Current Directory:", os.getcwd())
print("Directory Contents:", os.listdir('.'))

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
secrets_client = boto3.client('secretsmanager')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def get_openai_key():
    """Retrieve OpenAI API key from AWS Secrets Manager."""
    try:
        response = secrets_client.get_secret_value(
            SecretId="openai_key"
        )
        secrets = json.loads(response['SecretString'])
        return secrets['OPENAI_API_KEY']
    except Exception as e:
        logger.error(f"Failed to get OpenAI key: {str(e)}")
        raise

# Initialize OpenAI client
client = OpenAI(api_key=get_openai_key())

def get_prompt():
    """Load agile coach prompt template."""
    try:
        # First try to read from file
        prompt_path = Path(__file__).parent / "AgileExpertPrompt.md"
        
        with open(prompt_path, 'r') as f:
            return f.read()
            
    except Exception as e:
        print(f"Failed to read agile coach prompt: {str(e)}")
        # Fallback to hardcoded prompt
        return """
You are an Agile expert with the combined skills of an Agile Coach and a seasoned Scrum Master with over 15 years of experience. You have successfully guided Agile teams across diverse industries, working with a wide range of technologies, frameworks, and processes. Your primary assignment is to assist Product Owners in creating the best possible stories, ensuring they meet the needs of SAFe Scrum teams and adhere to Agile principles.

Your expertise enables you to:
1. Identify areas where stories can be improved for clarity and effectiveness.
2. Transform vague or incomplete stories into actionable, high-quality deliverables.
3. Apply the INVEST criteria to ensure the story is Independent, Negotiable, Valuable, Estimable, Small, and Testable.
4. Provide suggestions for further improvement based on best practices.

Please analyze the provided user story and provide feedback in the following JSON format:
{
    "score": "1-10 rating of the story quality",
    "strengths": ["List of story strengths"],
    "weaknesses": ["List of story weaknesses"],
    "suggestions": ["Specific suggestions for improvement"]
}
"""

def analyze_with_openai(content):
    try:
        # Log the prompt and content being sent
        prompt = get_prompt()
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(content)}
        ]
        
        print("=== OpenAI Request Details ===")
        print(f"Model: gpt-3.5-turbo")
        print(f"System Prompt: {prompt}")
        print(f"User Content: {json.dumps(content, indent=2)}")
        print(f"Full Messages Array: {json.dumps(messages, indent=2)}")
        print("============================")
        
        # Get OpenAI response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            response_format={ "type": "json_object" }
        )
        
        print(f"OpenAI raw response: {response}")
        
        # Parse OpenAI response
        analysis_response = json.loads(response.choices[0].message.content)
        print(f"Parsed OpenAI response: {json.dumps(analysis_response, indent=2)}")
        
        # Create the cleaned up structures
        content = {
            'title': analysis_response.get('title', content.get('title', '')),
            'story': analysis_response.get('story', content.get('story', '')),
            'acceptance_criteria': analysis_response.get('acceptance_criteria', [])
        }
        
        analysis = {
            'INVESTAnalysis': analysis_response.get('INVESTAnalysis', []),
            'Suggestions': analysis_response.get('Suggestions', [])
        }
        
        return {
            'content': content,
            'analysis': analysis
        }
        
    except Exception as e:
        print(f"=== Error in analyze_with_openai ===")
        print(f"Error type: {type(e)}")
        print(f"Error message: {str(e)}")
        print(f"Content received: {json.dumps(content, indent=2)}")
        print(f"Full traceback: {traceback.format_exc()}")
        print("===============================")
        raise

def handler(event, context):
    try:
        # Parse request
        body = json.loads(event.get('body', '{}'))
        story_id = body.get('story_id')
        tenant_id = body.get('tenant_id')
        
        current_time = datetime.now(UTC).isoformat().replace('+00:00', 'Z')
        
        # Initialize DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE', 'dev-agile-stories'))
        
        # Save original content in PENDING
        pending_item = {
            'story_id': story_id,
            'version': 'AGILE_COACH_PENDING',
            'tenant_id': tenant_id,
            'created_at': current_time,
            'updated_at': current_time,
            'content': {  # Original story content
                'title': body.get('title', ''),
                'story': body.get('story', ''),
                'description': body.get('description', ''),
                'acceptance_criteria': body.get('acceptance_criteria', [])
            },
            'analysis': {  # Empty until agent responds
                'content': {},
                'analysis': {}
            }
        }
        
        table.put_item(Item=pending_item)
        
        # Get AGILE_COACH analysis
        response = client.chat.completions.create(
            model=os.environ.get('GPT_MODEL', 'gpt-4-1106-preview'),
            messages=[
                {"role": "system", "content": get_prompt()},
                {"role": "user", "content": json.dumps(pending_item['content'])}
            ],
            response_format={ "type": "json_object" }
        )
        
        # Parse and store final response
        analysis = json.loads(response.choices[0].message.content)
        
        final_item = {
            'story_id': story_id,
            'version': 'AGILE_COACH',
            'tenant_id': tenant_id,
            'created_at': current_time,
            'updated_at': current_time,
            'content': pending_item['content'],  # Keep original content
            'analysis': analysis  # Agent's response with improved content and analysis
        }
        
        table.put_item(Item=final_item)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'story_id': story_id,
                'version': 'AGILE_COACH',
                'analysis': analysis
            })
        }
        
    except Exception as e:
        print(f"Error in handler: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

def get_story(event, context):
    """Get a story by ID and version.
    
    Note on DynamoDB Type Handling:
    - boto3's Table.get_item() automatically deserializes DynamoDB types (S, N, M, L) into Python types
    - No manual type conversion is needed for either reading or writing:
        - put_item(): Python types -> DynamoDB types (automatic)
        - get_item(): DynamoDB types -> Python types (automatic)
    """
    try:
        # Get path parameters
        story_id = event['pathParameters']['story_id']
        version = event.get('queryStringParameters', {}).get('version', 'INITIAL')
        
        # Initialize DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE', 'dev-agile-stories'))
        
        # Get item from DynamoDB - types are automatically deserialized
        response = table.get_item(
            Key={
                'story_id': story_id,
                'version': version
            }
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Story not found'})
            }
            
        # Return the item directly - no type conversion needed
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }
        
    except Exception as e:
        print(f"Error getting story: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        } 