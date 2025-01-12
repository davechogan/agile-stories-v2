import pytest
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any

from ..processor import AgentProcessor
from ..registry import AgentRegistry

# Test data
MOCK_STORY_DATA = {
    "title": "Test Story",
    "description": "As a user...",
    "acceptance_criteria": ["Given...", "When...", "Then..."]
}

MOCK_AGENT_CONFIG = {
    "name": "Backend Developer",
    "description": "Senior backend developer",
    "role": "backend_developer",
    "expertise_level": "senior",
    "model": "gpt-4-turbo-preview",
    "prompt_file": "backend_dev/BackendDevPrompt.md",
    "temperature": 0.7
}

MOCK_LAMBDA_RESPONSE = {
    "statusCode": 200,
    "body": '{"estimates": {"story_points": {"value": 5}}}'
}

class TestAgentProcessor:
    """Test suite for AgentProcessor class."""

    @pytest.fixture
    def mock_registry(self) -> Mock:
        """Create a mock registry."""
        registry = Mock(spec=AgentRegistry)
        registry.get_agent.return_value = MOCK_AGENT_CONFIG
        registry.get_estimation_team.return_value = [MOCK_AGENT_CONFIG]
        return registry

    @pytest.fixture
    def processor(self, mock_registry: Mock) -> AgentProcessor:
        """Create an AgentProcessor instance with a mock registry."""
        return AgentProcessor(mock_registry)

    @pytest.mark.asyncio
    async def test_process_with_agent_success(self, processor: AgentProcessor) -> None:
        """Test successful processing with an agent."""
        with patch('boto3.client') as mock_boto:
            # Setup mock Lambda client
            mock_lambda = AsyncMock()
            mock_lambda.invoke_async.return_value = {
                'Payload': Mock(read=lambda: MOCK_LAMBDA_RESPONSE['body'])
            }
            mock_boto.return_value = mock_lambda

            result = await processor.process_with_agent(
                'estimation',
                'backend_dev',
                MOCK_STORY_DATA
            )

            # Verify Lambda was called correctly
            mock_lambda.invoke_async.assert_called_once()
            assert result['estimates']['story_points']['value'] == 5

    @pytest.mark.asyncio
    async def test_process_with_agent_not_found(self, processor: AgentProcessor) -> None:
        """Test processing with non-existent agent."""
        processor.registry.get_agent.return_value = None
        
        with pytest.raises(ValueError) as exc_info:
            await processor.process_with_agent(
                'estimation',
                'nonexistent',
                MOCK_STORY_DATA
            )
        assert "not found" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_process_team_estimation(self, processor: AgentProcessor) -> None:
        """Test processing estimation with entire team."""
        with patch('boto3.client') as mock_boto:
            # Setup mock Lambda client
            mock_lambda = AsyncMock()
            mock_lambda.invoke_async.return_value = {
                'Payload': Mock(read=lambda: MOCK_LAMBDA_RESPONSE['body'])
            }
            mock_boto.return_value = mock_lambda

            results = await processor.process_team_estimation(MOCK_STORY_DATA)

            assert isinstance(results, list)
            assert len(results) == 1  # One agent in mock team
            assert results[0]['estimates']['story_points']['value'] == 5

    @pytest.mark.asyncio
    async def test_lambda_invocation_error(self, processor: AgentProcessor) -> None:
        """Test handling of Lambda invocation errors."""
        with patch('boto3.client') as mock_boto:
            mock_lambda = AsyncMock()
            mock_lambda.invoke_async.side_effect = Exception("Lambda error")
            mock_boto.return_value = mock_lambda

            with pytest.raises(RuntimeError) as exc_info:
                await processor.process_with_agent(
                    'estimation',
                    'backend_dev',
                    MOCK_STORY_DATA
                )
            assert "Lambda error" in str(exc_info.value) 