import boto3
import pytest
import os
import uuid
import json
from datetime import datetime, UTC
import time

@pytest.fixture
def setup_resources():
    # Initialize AWS clients
    sfn = boto3.client('stepfunctions')
    dynamodb = boto3.resource('dynamodb')
    lambda_client = boto3.client('lambda')
    
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    state_machine_arn = os.environ['STATE_MACHINE_ARN']
    story_state_handler_arn = os.environ['STORY_STATE_HANDLER_ARN']
    workflow_signal_handler_arn = os.environ['WORKFLOW_SIGNAL_HANDLER_ARN']
    
    return {
        'sfn': sfn,
        'table': table,
        'lambda_client': lambda_client,
        'state_machine_arn': state_machine_arn,
        'story_state_handler_arn': story_state_handler_arn,
        'workflow_signal_handler_arn': workflow_signal_handler_arn
    }

def test_story_state_handler(setup_resources):
    """Test that story_state_handler correctly stores tokens"""
    resources = setup_resources
    story_id = str(uuid.uuid4())
    mock_token = "MockToken123"
    
    # Invoke Lambda directly with test payload
    payload = {
        'story_id': story_id,
        'status': 'AGILE_COACH_PENDING',
        'taskToken': mock_token
    }
    
    response = resources['lambda_client'].invoke(
        FunctionName=resources['story_state_handler_arn'],
        Payload=json.dumps(payload)
    )
    
    # Verify token stored in DynamoDB
    item = resources['table'].get_item(
        Key={
            'story_id': story_id,
            'version': 'AGILE_COACH_PENDING'
        }
    )['Item']
    
    assert item['task_token'] == mock_token
    assert item['version'] == 'AGILE_COACH_PENDING'

def test_workflow_signal_handler(setup_resources):
    """Test that workflow_signal_handler correctly processes UI actions"""
    resources = setup_resources
    story_id = str(uuid.uuid4())
    mock_token = "MockToken456"
    
    # First store a token
    timestamp = datetime.now(UTC).isoformat()
    item = {
        'story_id': story_id,
        'version': 'AGILE_COACH_PENDING',
        'task_token': mock_token,
        'content': {'title': 'Test Story'},
        'created_at': timestamp,
        'updated_at': timestamp
    }
    resources['table'].put_item(Item=item)
    
    # Simulate UI action
    event = {
        'pathParameters': {
            'storyId': story_id,
            'action': 'agile-review'
        }
    }
    
    response = resources['lambda_client'].invoke(
        FunctionName=resources['workflow_signal_handler_arn'],
        Payload=json.dumps(event)
    )
    
    # Verify state transition
    updated_item = resources['table'].get_item(
        Key={
            'story_id': story_id,
            'version': 'TECH_REVIEW_PENDING'
        }
    )['Item']
    
    assert 'task_token' not in updated_item  # Token should be consumed

def test_complete_workflow(setup_resources):
    """Test the entire workflow end-to-end"""
    resources = setup_resources
    story_id = str(uuid.uuid4())
    
    # Start state machine execution
    execution = resources['sfn'].start_execution(
        stateMachineArn=resources['state_machine_arn'],
        input=json.dumps({'story_id': story_id})
    )
    
    # Wait for first wait state
    time.sleep(5)
    
    # Verify initial state
    item = resources['table'].get_item(
        Key={
            'story_id': story_id,
            'version': 'AGILE_COACH_PENDING'
        }
    )['Item']
    
    assert 'task_token' in item
    
    # Simulate UI actions through the workflow
    actions = ['agile-review', 'tech-review', 'estimation']
    for action in actions:
        event = {
            'pathParameters': {
                'storyId': story_id,
                'action': action
            }
        }
        
        resources['lambda_client'].invoke(
            FunctionName=resources['workflow_signal_handler_arn'],
            Payload=json.dumps(event)
        )
        
        time.sleep(5)  # Wait for state transition
    
    # Verify workflow completed
    execution_result = resources['sfn'].describe_execution(
        executionArn=execution['executionArn']
    )
    
    assert execution_result['status'] == 'SUCCEEDED'

def test_error_handling(setup_resources):
    """Test error scenarios and recovery"""
    resources = setup_resources
    story_id = str(uuid.uuid4())
    
    # Test invalid action
    event = {
        'pathParameters': {
            'storyId': story_id,
            'action': 'invalid-action'
        }
    }
    
    response = resources['lambda_client'].invoke(
        FunctionName=resources['workflow_signal_handler_arn'],
        Payload=json.dumps(event)
    )
    
    response_payload = json.loads(response['Payload'].read())
    assert response_payload['statusCode'] == 500
    
    # Test missing token
    event = {
        'pathParameters': {
            'storyId': str(uuid.uuid4()),  # Non-existent story
            'action': 'agile-review'
        }
    }
    
    response = resources['lambda_client'].invoke(
        FunctionName=resources['workflow_signal_handler_arn'],
        Payload=json.dumps(event)
    )
    
    response_payload = json.loads(response['Payload'].read())
    assert response_payload['statusCode'] == 500 