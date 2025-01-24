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
import traceback

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
    """Handle technical review requests.
    
    Version Flow:
    1. Save POST data as SENIOR_DEV_PENDING (this is the edited content from AgileReview page)
    2. Send basic story content to OpenAI
    3. Save OpenAI response as SENIOR_DEV
    """
    try:
        # Get and set OpenAI key first
        get_openai_key()
        
        # Parse POST request
        body = json.loads(event.get('body', '{}'))
        story_id = body.get('story_id')
        tenant_id = body.get('tenant_id')
        edited_content = body.get('analysis', {})  # This is the edited content from the frontend
        
        print("=== POST Content from Frontend ===")
        print(json.dumps(edited_content, indent=2))
        
        current_time = datetime.now(UTC).isoformat().replace('+00:00', 'Z')
        
        # Initialize DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE', 'dev-agile-stories'))
        
        # Save the edited content as SENIOR_DEV_PENDING
        pending_item = {
            'story_id': story_id,
            'version': 'SENIOR_DEV_PENDING',
            'tenant_id': tenant_id,
            'created_at': current_time,
            'updated_at': current_time,
            'content': edited_content
        }
        
        print("\n=== Saving SENIOR_DEV_PENDING ===")
        print(json.dumps(pending_item, indent=2))
        table.put_item(Item=pending_item)
        
        # Extract only what OpenAI needs
        story_content = {
            'title': edited_content.get('title', ''),
            'story': edited_content.get('story', ''),
            'acceptance_criteria': edited_content.get('acceptance_criteria', [])
        }
        
        print("\n=== Sending to OpenAI ===")
        print("Content:", json.dumps(story_content, indent=2))
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": get_technical_prompt()},
                {"role": "user", "content": json.dumps(story_content)}
            ],
            response_format={ "type": "json_object" }
        )
        
        # Parse OpenAI response
        tech_analysis = json.loads(response.choices[0].message.content)
        
        print("\n=== OpenAI Response ===")
        print(json.dumps(tech_analysis, indent=2))
        
        # Save final SENIOR_DEV version
        final_item = {
            'story_id': story_id,
            'version': 'SENIOR_DEV',
            'tenant_id': tenant_id,
            'created_at': current_time,
            'updated_at': current_time,
            'content': {
                'title': tech_analysis['title'],
                'story': tech_analysis['story'],
                'acceptance_criteria': tech_analysis['acceptance_criteria']
            },
            'analysis': {
                'ImplementationDetails': tech_analysis['ImplementationDetails'],
                'TechnicalAnalysis': tech_analysis['TechnicalAnalysis'],
                'RisksAndConsiderations': tech_analysis['RisksAndConsiderations'],
                'Recommendations': tech_analysis['Recommendations']
            }
        }
        
        print("\n=== Saving SENIOR_DEV ===")
        print(json.dumps(final_item, indent=2))
        
        table.put_item(Item=final_item)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'story_id': story_id,
                'version': 'SENIOR_DEV',
                'content': final_item['content'],
                'analysis': final_item['analysis']
            })
        }
        
    except Exception as e:
        print(f"\n=== Error in handler ===")
        print(f"Error type: {type(e)}")
        print(f"Error message: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 