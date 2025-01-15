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
import boto3
from botocore.exceptions import ClientError

# Initialize AWS client
dynamodb = boto3.resource('dynamodb')

def get_story(story_id, table):
    """
    Retrieve a story from DynamoDB by its ID and version
    
    Args:
        story_id (str): The story ID (HASH/Partition key)
        table: DynamoDB table object
        
    Returns:
        dict: The story item from DynamoDB
    """
    try:
        response = table.get_item(
            Key={
                'story_id': story_id,    # HASH/Partition key
                'version': 'ORIGINAL'     # RANGE/Sort key
            }
        )
        return response.get('Item')
    except ClientError as e:
        print(f"Error retrieving story: {e.response['Error']['Message']}")
        raise
    except Exception as e:
        print(f"Unexpected error retrieving story: {str(e)}")
        raise

def analyze_story(story):
    """
    Analyze the story content and return analysis results
    """
    # For now, just return a formatted version of the content
    return f"\nTitle: {story['content']['title']}\nDescription: {story['content']['description']}\nAcceptance Criteria:\n" + \
           "\n".join([f"- {criterion}" for criterion in story['content']['acceptance_criteria']])

def handler(event, context):
    try:
        # Initialize table inside handler
        table = dynamodb.Table(os.environ.get('STORIES_TABLE', 'dev-agile-stories'))
        
        for record in event['Records']:
            body = json.loads(record['body'])
            story_id = body['story_id']
            print(f"Processing story: {story_id}")
            
            # Get the original story
            original_story = get_story(story_id, table)
            print(f"Retrieved story: {json.dumps(original_story)}")
            
            # Process the story
            analysis = analyze_story(original_story)
            print(f"Analysis complete: {json.dumps(analysis)}")
            
            # Create the analyzed story object
            analyzed_story = {
                'story_id': story_id,
                'content': original_story['content'],
                'analysis': analysis,
                'version': 'AGILE_COACH'
            }
            
            # Save the analyzed story back to DynamoDB
            table.put_item(Item=analyzed_story)
            
    except KeyError as e:
        print(f"Error processing message: {str(e)}")
        print(f"Event: {json.dumps(event)}")
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise 