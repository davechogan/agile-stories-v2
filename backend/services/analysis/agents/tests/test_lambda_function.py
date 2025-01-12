import pytest
from unittest.mock import patch, Mock
import json

from ..lambda_function import handler

# Test data
MOCK_EVENT = {
    "story_data": {
        "title": "Test Story",
        "description": "As a user...",
        "acceptance_criteria": ["Given...", "When...", "Then..."]
    },
    "agent_config": {
        "name": "Backend Developer",
        "model": "gpt-4-turbo-preview",
        "temperature": 0.7
    },
    "prompt_file": "backend_dev/BackendDevPrompt.md"
}

MOCK_OPENAI_RESPONSE = Mock(
    choices=[
        Mock(
            message=Mock(
                content=json.dumps({
                    "estimates": {
                        "story_points": {
                            "value": 5,
                            "confidence": "HIGH",
                            "explanation": "Clear requirements"
                        }
                    }
                })
            )
        )
    ]
)

class TestLambdaFunction:
    """Test suite for Lambda function handler."""

    def test_successful_processing(self) -> None:
        """Test successful story processing."""
        with patch('openai.OpenAI') as mock_openai:
            # Setup mock OpenAI client
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = MOCK_OPENAI_RESPONSE
            mock_openai.return_value = mock_client

            # Mock prompt loading
            with patch('builtins.open', mock_open(read_data="Test prompt")):
                response = handler(MOCK_EVENT, {})

                assert response['statusCode'] == 200
                body = json.loads(response['body'])
                assert body['estimates']['story_points']['value'] == 5

    def test_missing_required_fields(self) -> None:
        """Test handling of missing required fields in event."""
        invalid_event = {
            "story_data": {}  # Missing other required fields
        }

        response = handler(invalid_event, {})
        assert response['statusCode'] == 500
        assert 'error' in json.loads(response['body'])

    def test_openai_api_error(self) -> None:
        """Test handling of OpenAI API errors."""
        with patch('openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_client.chat.completions.create.side_effect = Exception("API Error")
            mock_openai.return_value = mock_client

            response = handler(MOCK_EVENT, {})
            assert response['statusCode'] == 500
            assert 'API Error' in json.loads(response['body'])['error']

    def test_invalid_openai_response(self) -> None:
        """Test handling of invalid JSON in OpenAI response."""
        with patch('openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_response = Mock(
                choices=[
                    Mock(message=Mock(content="Invalid JSON"))
                ]
            )
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client

            response = handler(MOCK_EVENT, {})
            assert response['statusCode'] == 500
            assert 'error' in json.loads(response['body']) 