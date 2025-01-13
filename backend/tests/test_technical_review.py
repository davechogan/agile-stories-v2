"""
Unit tests for the Technical Review Lambda
Tests the queueing of stories for senior developer review
"""

import pytest
from unittest.mock import Mock, patch
import json
from src.technical_review.app import handler

@pytest.fixture
def valid_event():
    return {
        'body': json.dumps({
            'story_id': 'test-123'
        })
    }

@pytest.fixture
def mock_dynamodb():
    with patch('boto3.resource') as mock:
        mock_table = Mock()
        mock.return_value.Table.return_value = mock_table
        
        # Mock successful story retrieval
        mock_table.get_item.return_value = {
            'Item': {
                'story_id': 'test-123',
                'version': 'AGILE_COACH',
                'content': {
                    'improved_story': {
                        'title': 'Test Story',
                        'description': 'As a user...',
                        'acceptance_criteria': ['Given...', 'When...', 'Then...']
                    }
                }
            }
        }
        
        yield mock_table

@pytest.fixture
def mock_sqs():
    with patch('boto3.client') as mock:
        mock_client = Mock()
        mock.return_value = mock_client
        yield mock_client

def test_successful_queue(valid_event, mock_dynamodb, mock_sqs):
    # Act
    response = handler(valid_event, None)
    
    # Assert
    assert response['statusCode'] == 200
    response_body = json.loads(response['body'])
    assert response_body['story_id'] == 'test-123'
    assert 'message' in response_body
    
    # Verify DynamoDB check
    mock_dynamodb.get_item.assert_called_once_with(
        Key={
            'story_id': 'test-123',
            'version': 'AGILE_COACH'
        }
    )
    
    # Verify SQS message
    mock_sqs.return_value.send_message.assert_called_once()
    sqs_message = json.loads(
        mock_sqs.return_value.send_message.call_args[1]['MessageBody']
    )
    assert sqs_message['story_id'] == 'test-123'

def test_story_not_found(valid_event, mock_dynamodb, mock_sqs):
    # Arrange
    mock_dynamodb.get_item.return_value = {}  # No Item in response
    
    # Act
    response = handler(valid_event, None)
    
    # Assert
    assert response['statusCode'] == 404
    assert 'error' in json.loads(response['body'])
    mock_sqs.return_value.send_message.assert_not_called()

def test_invalid_input():
    # Arrange
    event = {
        'body': 'invalid json'
    }
    
    # Act
    response = handler(event, None)
    
    # Assert
    assert response['statusCode'] == 500
    assert 'error' in json.loads(response['body'])

def test_dynamodb_error(valid_event, mock_dynamodb, mock_sqs):
    # Arrange
    mock_dynamodb.get_item.side_effect = Exception("DynamoDB Error")
    
    # Act
    response = handler(valid_event, None)
    
    # Assert
    assert response['statusCode'] == 500
    error_message = json.loads(response['body'])['error']
    assert "Database error" in error_message
    mock_sqs.return_value.send_message.assert_not_called()

def test_sqs_error(valid_event, mock_dynamodb, mock_sqs):
    # Arrange
    mock_sqs.return_value.send_message.side_effect = Exception("SQS Error")
    
    # Act
    response = handler(valid_event, None)
    
    # Assert
    assert response['statusCode'] == 500
    error_message = json.loads(response['body'])['error']
    assert "Queue error" in error_message 