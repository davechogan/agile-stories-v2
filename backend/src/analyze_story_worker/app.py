"""
Agile Coach Analysis Worker Lambda

This Lambda processes stories from SQS, sending them to the OpenAI API
for Agile Coach analysis and storing the results in DynamoDB.

Flow:
1. Receives message from SQS with story_id
2. Retrieves original story from DynamoDB
3. Sends to OpenAI for Agile Coach analysis
4. Stores analysis results in DynamoDB

Environment Variables:
    DYNAMODB_TABLE: DynamoDB table name
    OPENAI_API_KEY: OpenAI API key
"""

import json
import os
from datetime import datetime
import boto3
from openai import OpenAI

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def get_agile_coach_prompt():
    return """You are an experienced Agile Coach reviewing a user story.
    Analyze the story and provide:
    1. An improved version of the story
    2. INVEST analysis
    3. Specific suggestions for improvement
    
    Respond with a JSON object containing:
    {
        "improved_story": {
            "title": "string",
            "description": "string",
            "acceptance_criteria": ["string"]
        },
        "invest_analysis": [
            {
                "letter": "I",
                "title": "Independent",
                "content": "Analysis of independence"
            },
            ...
        ],
        "suggestions": [
            {
                "title": "Suggestion title",
                "content": "Detailed suggestion"
            }
        ]
    }"""

def handler(event, context):
    try:
        for record in event['Records']:
            # Get message from SQS
            message = json.loads(record['body'])
            story_id = message['story_id']
            
            # Get original story from DynamoDB
            response = table.get_item(
                Key={
                    'story_id': story_id,
                    'version': 'ORIGINAL'
                }
            )
            original_story = response['Item']
            
            # Send to OpenAI
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": get_agile_coach_prompt()},
                    {"role": "user", "content": json.dumps(original_story['content'])}
                ]
            )
            
            # Store analysis
            analysis_item = {
                'story_id': story_id,
                'version': 'AGILE_COACH',
                'content': json.loads(response.choices[0].message.content),
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            table.put_item(Item=analysis_item)
            
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        raise 