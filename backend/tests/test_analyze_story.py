import pytest
from unittest.mock import Mock, patch
import json
from src.analyze_story.app import handler
import boto3
from moto import mock_secretsmanager

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

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    import os
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

@pytest.fixture
def secretsmanager_client(aws_credentials):
    with mock_secretsmanager():
        client = boto3.client('secretsmanager', region_name='us-east-1')
        # Create test secret
        client.create_secret(
            Name='openai_key',
            SecretString='test-openai-key'
        )
        yield client

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