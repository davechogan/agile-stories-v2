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
        return secrets['OPENAI_API_KEY']
    except Exception as e:
        print(f"Failed to get OpenAI key: {str(e)}")
        raise

def handler(event, context):
    try:
        print("Event received:", json.dumps(event))
        
        # Get story_id from path parameters
        story_id = event.get('pathParameters', {}).get('storyId')
        
        # Get tenant_id from body
        body = json.loads(event.get('body', '{}'))
        tenant_id = body.get('tenant_id')
        
        print(f"Processing story_id: {story_id}, tenant_id: {tenant_id}")
        
        if not story_id:
            print("Error: Missing story_id in path parameters")
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Missing story_id in path parameters'
                })
            }
            
        if not tenant_id:
            print("Error: Missing tenant_id in request body")
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Missing tenant_id in request body'
                })
            }
            
        current_time = datetime.now(UTC).isoformat().replace('+00:00', 'Z')
        
        # Initialize DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE', 'dev-agile-stories'))
        
        print(f"Processing technical review for story_id: {story_id}")
        
        # Get the AGILE_COACH version to get both content and analysis
        try:
            response = table.get_item(
                Key={
                    'story_id': story_id,
                    'version': 'AGILE_COACH'
                }
            )
            if 'Item' not in response:
                raise Exception(f"Story {story_id} not found")
                
            agile_coach_version = response['Item']
            content = agile_coach_version['content']
            analysis = agile_coach_version['analysis']  # Get the analysis with improvements
            
            # Create enriched content with improvements
            enriched_content = {
                **content,  # Original content
                'improvedTitle': analysis.get('ImprovedTitle'),
                'improvedStory': analysis.get('ImprovedStory'),
                'improvedAcceptanceCriteria': analysis.get('ImprovedAcceptanceCriteria'),
                'INVESTAnalysis': analysis.get('INVESTAnalysis'),
                'suggestions': analysis.get('Suggestions')
            }
            
        except Exception as e:
            print(f"Error getting story content and analysis: {str(e)}")
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': f'Story not found: {str(e)}'
                })
            }
        
        # Save as SENIOR_DEV_PENDING with enriched content
        pending_item = {
            'story_id': story_id,
            'tenant_id': tenant_id,
            'version': 'SENIOR_DEV_PENDING',
            'content': enriched_content,  # Use the enriched content
            'created_at': current_time,
            'updated_at': current_time
        }
        table.put_item(Item=pending_item)
        
        # Get OpenAI analysis using key from SSM
        openai.api_key = get_openai_key()
        client = openai.Client(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": get_technical_prompt()},
                {"role": "user", "content": json.dumps(content)}
            ]
        )
        
        analysis = response.choices[0].message.content
        
        # Save as SENIOR_DEV
        analysis_item = {
            'story_id': story_id,
            'tenant_id': tenant_id,
            'version': 'SENIOR_DEV',
            'content': content,
            'analysis': analysis,
            'created_at': current_time,
            'updated_at': current_time
        }
        table.put_item(Item=analysis_item)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'success',
                'story_id': story_id
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