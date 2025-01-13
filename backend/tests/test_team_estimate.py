"""
Unit tests for the Team Estimation Lambda
Tests the queueing of stories for team member estimation
"""

import pytest
from unittest.mock import Mock, patch
import json
import os
from src.team_estimate.app import handler

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
                'version': 'SENIOR_DEV',
                'content': {
                    'technical_analysis': {
                        'implementation': [],
                        'architecture_impact': {},
                        'risks': [],
                        'dependencies': {}
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

@pytest.fixture
def mock_env_vars():
    original_env = dict(os.environ)
    os.environ['TEAM_MEMBERS'] = json.dumps([
        {"id": "member1", "role": "developer"},
        {"id": "member2", "role": "tester"},
        {"id": "member3", "role": "architect"}
    ])
    yield
    os.environ.clear()
    os.environ.update(original_env)

def test_successful_queue(valid_event, mock_dynamodb, mock_sqs, mock_env_vars):
    # Act
    response = handler(valid_event, None)
    
    # Assert
    assert response['statusCode'] == 200
    response_body = json.loads(response['body'])
    assert response_body['story_id'] == 'test-123'
    assert 'message' in response_body
    assert len(response_body['queued_members']) == 3
    
    # Verify DynamoDB check
    mock_dynamodb.get_item.assert_called_once_with(
        Key={
            'story_id': 'test-123',
            'version': 'SENIOR_DEV'
        }
    )
    
    # Verify SQS messages
    assert mock_sqs.return_value.send_message.call_count == 3
    
    # Verify message content for each team member
    calls = mock_sqs.return_value.send_message.call_args_list
    sent_messages = [
        json.loads(call[1]['MessageBody'])
        for call in calls
    ]
    
    assert any(m['member_id'] == 'member1' and m['role'] == 'developer' for m in sent_messages)
    assert any(m['member_id'] == 'member2' and m['role'] == 'tester' for m in sent_messages)
    assert any(m['member_id'] == 'member3' and m['role'] == 'architect' for m in sent_messages)

def test_story_not_found(valid_event, mock_dynamodb, mock_sqs, mock_env_vars):
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

def test_dynamodb_error(valid_event, mock_dynamodb, mock_sqs, mock_env_vars):
    # Arrange
    mock_dynamodb.get_item.side_effect = Exception("DynamoDB Error")
    
    # Act
    response = handler(valid_event, None)
    
    # Assert
    assert response['statusCode'] == 500
    error_message = json.loads(response['body'])['error']
    assert "Database error" in error_message
    mock_sqs.return_value.send_message.assert_not_called()

def test_sqs_error(valid_event, mock_dynamodb, mock_sqs, mock_env_vars):
    # Arrange
    mock_sqs.return_value.send_message.side_effect = Exception("SQS Error")
    
    # Act
    response = handler(valid_event, None)
    
    # Assert
    assert response['statusCode'] == 500
    error_message = json.loads(response['body'])['error']
    assert "Queue error" in error_message

def test_invalid_team_members_env(valid_event, mock_dynamodb, mock_sqs):
    # Arrange
    os.environ['TEAM_MEMBERS'] = 'invalid json'
    
    # Act
    response = handler(valid_event, None)
    
    # Assert
    assert response['statusCode'] == 500
    assert 'error' in json.loads(response['body'])
    mock_sqs.return_value.send_message.assert_not_called() 