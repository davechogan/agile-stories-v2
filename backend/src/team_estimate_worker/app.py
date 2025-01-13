"""
Team Estimation Worker Lambda

This Lambda processes estimation requests for individual team members, sending stories
to OpenAI with role-specific prompts and storing their estimates.

Flow:
1. Receives message from SQS with story_id and member details
2. Retrieves SENIOR_DEV version from DynamoDB
3. Sends to OpenAI with role-specific prompt
4. Stores estimate in DynamoDB as TEAM_ESTIMATES#{member_id}

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

def get_role_prompt(role):
    """Get role-specific estimation prompt"""
    base_prompt = """You are an experienced {role} estimating the effort for a user story.
    Consider the technical analysis and provide:
    1. Story point estimate (1, 2, 3, 5, 8, 13)
    2. Detailed justification for your estimate
    
    Focus on:
    """
    
    role_specifics = {
        'developer': """
        - Implementation complexity
        - Code changes required
        - Technical debt impact
        - Development environment setup
        - Unit testing effort""",
        
        'tester': """
        - Test case complexity
        - Test data requirements
        - Integration testing needs
        - Edge cases to consider
        - Test automation effort""",
        
        'architect': """
        - System-wide impact
        - Scalability considerations
        - Security implications
        - Infrastructure changes
        - Cross-service dependencies"""
    }
    
    return base_prompt.format(role=role) + role_specifics.get(role, "")

def handler(event, context):
    try:
        for record in event['Records']:
            # Get message from SQS
            message = json.loads(record['body'])
            story_id = message['story_id']
            member_id = message['member_id']
            role = message['role']
            
            # Get SENIOR_DEV version from DynamoDB
            response = table.get_item(
                Key={
                    'story_id': story_id,
                    'version': 'SENIOR_DEV'
                }
            )
            tech_review = response['Item']
            
            # Get OpenAI API key from Secrets Manager
            openai_api_key = get_secret()
            client = OpenAI(api_key=openai_api_key)
            
            # Send to OpenAI with role-specific prompt
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": get_role_prompt(role)},
                    {"role": "user", "content": json.dumps({
                        "story": tech_review['content']['technical_analysis'],
                        "role": role,
                        "instructions": "Provide estimate as JSON with 'estimate' (number) and 'justification' (string)"
                    })}
                ]
            )
            
            # Parse and validate estimate
            estimate_content = json.loads(response.choices[0].message.content)
            if not isinstance(estimate_content['estimate'], (int, float)):
                raise ValueError("Estimate must be a number")
            
            # Store estimate
            estimate_item = {
                'story_id': story_id,
                'version': f'TEAM_ESTIMATES#{member_id}',
                'content': {
                    'estimate': estimate_content['estimate'],
                    'justification': estimate_content['justification'],
                    'role': role
                },
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            table.put_item(Item=estimate_item)
            
            # Check if all team members have estimated
            team_members = json.loads(os.environ['TEAM_MEMBERS'])
            all_estimates = []
            
            for member in team_members:
                try:
                    estimate_response = table.get_item(
                        Key={
                            'story_id': story_id,
                            'version': f'TEAM_ESTIMATES#{member["id"]}'
                        }
                    )
                    if 'Item' in estimate_response:
                        all_estimates.append({
                            'member_id': member['id'],
                            'role': member['role'],
                            'estimate': estimate_response['Item']['content']['estimate']
                        })
                except Exception as e:
                    print(f"Error checking estimate for {member['id']}: {str(e)}")
            
            # If all members have estimated, create FINAL version
            if len(all_estimates) == len(team_members):
                average_estimate = sum(e['estimate'] for e in all_estimates) / len(all_estimates)
                
                final_item = {
                    'story_id': story_id,
                    'version': 'FINAL',
                    'content': {
                        'average_estimate': average_estimate,
                        'team_estimates': all_estimates
                    },
                    'created_at': datetime.utcnow().isoformat(),
                    'updated_at': datetime.utcnow().isoformat()
                }
                
                table.put_item(Item=final_item)
            
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        raise 