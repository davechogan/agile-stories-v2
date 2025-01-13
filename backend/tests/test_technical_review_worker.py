"""
Unit tests for the Technical Review Worker Lambda
Tests the processing of SQS messages and Senior Dev AI analysis
"""

import pytest
from unittest.mock import Mock, patch, ANY
import json
from src.technical_review_worker.app import handler

@pytest.fixture
def sqs_event():
    return {
        'Records': [{
            'body': json.dumps({
                'story_id': 'test-123'
            })
        }]
    }

@pytest.fixture
def mock_dynamodb():
    with patch('boto3.resource') as mock:
        mock_table = Mock()
        mock.return_value.Table.return_value = mock_table
        
        # Mock the AGILE_COACH story retrieval
        mock_table.get_item.return_value = {
            'Item': {
                'story_id': 'test-123',
                'version': 'AGILE_COACH',
                'content': {
                    'improved_story': {
                        'title': 'Test Story',
                        'description': 'As a user...',
                        'acceptance_criteria': ['Given...', 'When...', 'Then...']
                    },
                    'invest_analysis': [
                        {
                            'letter': 'I',
                            'title': 'Independent',
                            'content': 'Analysis'
                        }
                    ]
                }
            }
        }
        
        yield mock_table

@pytest.fixture
def mock_openai():
    with patch('openai.OpenAI') as mock:
        mock_client = Mock()
        mock.return_value = mock_client
        
        # Mock the OpenAI response
        mock_response = Mock()
        mock_response.choices = [
            Mock(
                message=Mock(
                    content=json.dumps({
                        'technical_analysis': {
                            'implementation': [
                                {
                                    'area': 'Backend',
                                    'considerations': 'Need API endpoint',
                                    'complexity': 'MEDIUM'
                                }
                            ],
                            'architecture_impact': {
                                'description': 'Minimal impact',
                                'affected_components': ['API', 'Database'],
                                'data_flow_changes': ['New endpoint']
                            },
                            'risks': [
                                {
                                    'title': 'Performance',
                                    'description': 'High load consideration',
                                    'mitigation': 'Caching',
                                    'severity': 'LOW'
                                }
                            ],
                            'dependencies': {
                                'technical': ['API Gateway'],
                                'business': ['User permissions'],
                                'prerequisites': ['Authentication']
                            }
                        }
                    })
                )
            )
        ]
        mock_client.chat.completions.create.return_value = mock_response
        
        yield mock_client

def test_successful_processing(sqs_event, mock_dynamodb, mock_openai):
    # Act
    handler(sqs_event, None)
    
    # Assert
    # Check DynamoDB was queried for AGILE_COACH version
    mock_dynamodb.get_item.assert_called_once_with(
        Key={
            'story_id': 'test-123',
            'version': 'AGILE_COACH'
        }
    )
    
    # Check OpenAI was called
    mock_openai.chat.completions.create.assert_called_once()
    
    # Check technical analysis was stored
    mock_dynamodb.put_item.assert_called_once()
    put_item_args = mock_dynamodb.put_item.call_args[1]['Item']
    assert put_item_args['story_id'] == 'test-123'
    assert put_item_args['version'] == 'SENIOR_DEV'
    assert 'content' in put_item_args
    assert 'technical_analysis' in put_item_args['content']
    assert 'created_at' in put_item_args
    assert 'updated_at' in put_item_args

def test_dynamodb_get_error(sqs_event, mock_dynamodb, mock_openai):
    # Arrange
    mock_dynamodb.get_item.side_effect = Exception("DynamoDB Error")
    
    # Act & Assert
    with pytest.raises(Exception) as exc:
        handler(sqs_event, None)
    assert str(exc.value) == "DynamoDB Error"
    mock_openai.chat.completions.create.assert_not_called()

def test_openai_error(sqs_event, mock_dynamodb, mock_openai):
    # Arrange
    mock_openai.chat.completions.create.side_effect = Exception("OpenAI Error")
    
    # Act & Assert
    with pytest.raises(Exception) as exc:
        handler(sqs_event, None)
    assert str(exc.value) == "OpenAI Error"
    mock_dynamodb.put_item.assert_not_called()

def test_invalid_openai_response(sqs_event, mock_dynamodb, mock_openai):
    # Arrange
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="Invalid JSON"))]
    mock_openai.chat.completions.create.return_value = mock_response
    
    # Act & Assert
    with pytest.raises(json.JSONDecodeError):
        handler(sqs_event, None)
    mock_dynamodb.put_item.assert_not_called()

def test_missing_agile_coach_version(sqs_event, mock_dynamodb, mock_openai):
    # Arrange
    mock_dynamodb.get_item.return_value = {}  # No Item in response
    
    # Act & Assert
    with pytest.raises(KeyError):
        handler(sqs_event, None)
    mock_openai.chat.completions.create.assert_not_called() 