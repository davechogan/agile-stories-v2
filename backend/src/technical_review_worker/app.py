"""
Technical Review Worker Lambda

This Lambda processes stories from the technical review queue, sending them to the OpenAI API
for Senior Developer analysis and storing the results in DynamoDB.

Flow:
1. Receives message from SQS with story_id
2. Retrieves AGILE_COACH version from DynamoDB
3. Sends to OpenAI for Senior Dev analysis
4. Stores analysis results in DynamoDB

Environment Variables:
    DYNAMODB_TABLE: DynamoDB table name
    OPENAI_API_KEY: OpenAI API key
"""

import json
import os
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from openai import OpenAI

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def get_secret():
    secret_name = "openai_key"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        return get_secret_value_response['SecretString']
    except ClientError as e:
        raise e

def get_senior_dev_prompt():
    return """You are a Senior Developer reviewing a user story.
    Analyze the story from a technical perspective and provide:
    1. Technical implementation considerations
    2. Architecture impact analysis
    3. Potential technical risks
    4. Dependencies and prerequisites
    
    Respond with a JSON object containing:
    {
        "technical_analysis": {
            "implementation": [
                {
                    "area": "string",
                    "considerations": "string",
                    "complexity": "HIGH|MEDIUM|LOW"
                }
            ],
            "architecture_impact": {
                "description": "string",
                "affected_components": ["string"],
                "data_flow_changes": ["string"]
            },
            "risks": [
                {
                    "title": "string",
                    "description": "string",
                    "mitigation": "string",
                    "severity": "HIGH|MEDIUM|LOW"
                }
            ],
            "dependencies": {
                "technical": ["string"],
                "business": ["string"],
                "prerequisites": ["string"]
            }
        }
    }"""

def handler(event, context):
    try:
        # Get OpenAI API key from Secrets Manager
        openai_api_key = get_secret()
        client = OpenAI(api_key=openai_api_key)
        
        for record in event['Records']:
            # Get message from SQS
            message = json.loads(record['body'])
            story_id = message['story_id']
            
            # Get AGILE_COACH version from DynamoDB
            response = table.get_item(
                Key={
                    'story_id': story_id,
                    'version': 'AGILE_COACH'
                }
            )
            agile_coach_story = response['Item']
            
            # Send to OpenAI
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": get_senior_dev_prompt()},
                    {"role": "user", "content": json.dumps(agile_coach_story['content'])}
                ]
            )
            
            # Store analysis
            analysis_item = {
                'story_id': story_id,
                'version': 'SENIOR_DEV',
                'content': json.loads(response.choices[0].message.content),
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            table.put_item(Item=analysis_item)
            
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        raise 