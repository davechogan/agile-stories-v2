import boto3
import pytest
import os
import uuid
from datetime import datetime, UTC

@pytest.fixture
def dynamodb_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def test_token_storage_and_retrieval(dynamodb_table):
    # Create test data
    story_id = str(uuid.uuid4())
    mock_token = "MockTaskToken123"
    timestamp = datetime.now(UTC).isoformat()
    
    # Test writing with token
    item = {
        'story_id': story_id,
        'version': 'AGILE_COACH_PENDING',
        'task_token': mock_token,
        'content': {
            'title': 'Test Story',
            'description': 'Test Description'
        },
        'created_at': timestamp,
        'updated_at': timestamp
    }
    
    try:
        # Write to DynamoDB
        dynamodb_table.put_item(Item=item)
        
        # Read back and verify
        response = dynamodb_table.get_item(
            Key={
                'story_id': story_id,
                'version': 'AGILE_COACH_PENDING'
            }
        )
        
        stored_item = response['Item']
        assert stored_item['task_token'] == mock_token
        assert stored_item['story_id'] == story_id
        
        # Test updating token
        new_token = "NewTaskToken456"
        dynamodb_table.update_item(
            Key={
                'story_id': story_id,
                'version': 'AGILE_COACH_PENDING'
            },
            UpdateExpression='SET task_token = :token, updated_at = :time',
            ExpressionAttributeValues={
                ':token': new_token,
                ':time': datetime.now(UTC).isoformat()
            }
        )
        
        # Verify update
        response = dynamodb_table.get_item(
            Key={
                'story_id': story_id,
                'version': 'AGILE_COACH_PENDING'
            }
        )
        
        updated_item = response['Item']
        assert updated_item['task_token'] == new_token
        
    finally:
        # Cleanup
        dynamodb_table.delete_item(
            Key={
                'story_id': story_id,
                'version': 'AGILE_COACH_PENDING'
            }
        ) 