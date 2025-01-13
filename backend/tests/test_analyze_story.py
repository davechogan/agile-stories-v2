import pytest
from unittest.mock import Mock, patch
import json
from src.analyze_story.app import handler

@pytest.fixture
def valid_event():
    return {
        'body': json.dumps({
            'title': 'Test Story',
            'description': 'As a user...',
            'acceptance_criteria': ['Given...', 'When...', 'Then...']
        })
    }

@pytest.fixture
def mock_dynamodb():
    with patch('boto3.resource') as mock:
        yield mock

@pytest.fixture
def mock_sqs():
    with patch('boto3.client') as mock:
        yield mock

def test_successful_story_submission(valid_event, mock_dynamodb, mock_sqs):
    # Arrange
    mock_table = Mock()
    mock_dynamodb.return_value.Table.return_value = mock_table
    
    # Act
    response = handler(valid_event, None)
    
    # Assert
    assert response['statusCode'] == 200
    response_body = json.loads(response['body'])
    assert 'story_id' in response_body
    assert 'message' in response_body
    
    # Verify DynamoDB call
    mock_table.put_item.assert_called_once()
    
    # Verify SQS call
    mock_sqs.return_value.send_message.assert_called_once()

def test_invalid_input(mock_dynamodb, mock_sqs):
    # Arrange
    event = {'body': 'invalid json'}
    
    # Act
    response = handler(event, None)
    
    # Assert
    assert response['statusCode'] == 500
    assert 'error' in json.loads(response['body']) 