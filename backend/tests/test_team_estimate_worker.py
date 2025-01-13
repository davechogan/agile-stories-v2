"""
Unit tests for the Team Estimation Worker Lambda
Tests the processing of estimation requests and result aggregation
"""

import pytest
from unittest.mock import Mock, patch, ANY
import json
import os
from src.team_estimate_worker.app import handler

@pytest.fixture
def sqs_event():
    return {
        'Records': [{
            'body': json.dumps({
                'story_id': 'test-123',
                'member_id': 'member1',
                'role': 'developer'
            })
        }]
    }

@pytest.fixture
def mock_dynamodb():
    with patch('boto3.resource') as mock:
        mock_table = Mock()
        mock.return_value.Table.return_value = mock_table
        
        # Mock the SENIOR_DEV story retrieval
        mock_table.get_item.return_value = {
            'Item': {
                'story_id': 'test-123',
                'version': 'SENIOR_DEV',
                'content': {
                    'technical_analysis': {
                        'implementation': [
                            {
                                'area': 'Backend',
                                'considerations': 'API changes',
                                'complexity': 'MEDIUM'
                            }
                        ],
                        'architecture_impact': {
                            'description': 'Minimal impact',
                            'affected_components': ['API']
                        }
                    }
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
                        'estimate': 5,
                        'justification': 'Medium complexity due to API changes'
                    })
                )
            )
        ]
        mock_client.chat.completions.create.return_value = mock_response
        
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

def test_successful_estimation(sqs_event, mock_dynamodb, mock_openai, mock_env_vars):
    # Act
    handler(sqs_event, None)
    
    # Assert
    # Check DynamoDB was queried for SENIOR_DEV version
    mock_dynamodb.get_item.assert_any_call(
        Key={
            'story_id': 'test-123',
            'version': 'SENIOR_DEV'
        }
    )
    
    # Check OpenAI was called
    mock_openai.chat.completions.create.assert_called_once()
    
    # Check estimate was stored
    put_calls = [
        call for call in mock_dynamodb.put_item.call_args_list
        if call[1]['Item']['version'] == 'TEAM_ESTIMATES#member1'
    ]
    assert len(put_calls) == 1
    estimate_item = put_calls[0][1]['Item']
    assert estimate_item['story_id'] == 'test-123'
    assert estimate_item['content']['estimate'] == 5
    assert estimate_item['content']['role'] == 'developer'

def test_final_version_creation(sqs_event, mock_dynamodb, mock_openai, mock_env_vars):
    # Arrange
    # Mock existing estimates for other team members
    def get_item_side_effect(Key):
        if Key['version'] == 'SENIOR_DEV':
            return {
                'Item': {
                    'story_id': 'test-123',
                    'version': 'SENIOR_DEV',
                    'content': {'technical_analysis': {}}
                }
            }
        elif Key['version'].startswith('TEAM_ESTIMATES#'):
            return {
                'Item': {
                    'content': {
                        'estimate': 5,
                        'role': 'developer'
                    }
                }
            }
        return {}
    
    mock_dynamodb.get_item.side_effect = get_item_side_effect
    
    # Act
    handler(sqs_event, None)
    
    # Assert
    # Check FINAL version was created
    put_calls = [
        call for call in mock_dynamodb.put_item.call_args_list
        if call[1]['Item']['version'] == 'FINAL'
    ]
    assert len(put_calls) == 1
    final_item = put_calls[0][1]['Item']
    assert final_item['content']['average_estimate'] == 5
    assert len(final_item['content']['team_estimates']) == 3

def test_invalid_estimate_response(sqs_event, mock_dynamodb, mock_openai, mock_env_vars):
    # Arrange
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content=json.dumps({
            'estimate': 'invalid',
            'justification': 'test'
        })))
    ]
    mock_openai.chat.completions.create.return_value = mock_response
    
    # Act & Assert
    with pytest.raises(ValueError):
        handler(sqs_event, None)

def test_dynamodb_error(sqs_event, mock_dynamodb, mock_openai, mock_env_vars):
    # Arrange
    mock_dynamodb.get_item.side_effect = Exception("DynamoDB Error")
    
    # Act & Assert
    with pytest.raises(Exception) as exc:
        handler(sqs_event, None)
    assert str(exc.value) == "DynamoDB Error"

def test_openai_error(sqs_event, mock_dynamodb, mock_openai, mock_env_vars):
    # Arrange
    mock_openai.chat.completions.create.side_effect = Exception("OpenAI Error")
    
    # Act & Assert
    with pytest.raises(Exception) as exc:
        handler(sqs_event, None)
    assert str(exc.value) == "OpenAI Error"

def test_missing_team_members_env(sqs_event, mock_dynamodb, mock_openai):
    # Act & Assert
    with pytest.raises(KeyError):
        handler(sqs_event, None) 