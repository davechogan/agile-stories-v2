import os
import pytest
from unittest.mock import mock_open, patch
from typing import Dict, Any

from ..registry import AgentRegistry

# Test data
VALID_CORE_CONFIG = """
agents:
  agile_expert:
    name: "Agile Expert"
    description: "Expert in agile practices and story refinement"
    model: "gpt-4-turbo-preview"
    prompt_file: "agile_expert/AgileExpertPrompt.md"
    temperature: 0.7
"""

VALID_ESTIMATION_CONFIG = """
agents:
  backend_dev:
    name: "Backend Developer"
    description: "Senior backend developer"
    role: "backend_developer"
    expertise_level: "senior"
    model: "gpt-4-turbo-preview"
    prompt_file: "backend_dev/BackendDevPrompt.md"
    temperature: 0.7
"""

INVALID_CONFIG = """
agents:
  invalid_agent:
    name: "Invalid Agent"
"""

class TestAgentRegistry:
    """Test suite for AgentRegistry class."""

    @pytest.fixture
    def config_dir(self, tmp_path) -> str:
        """Create a temporary config directory with test files."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        return str(config_dir)

    @pytest.fixture
    def mock_prompt_content(self) -> str:
        """Mock content for prompt files."""
        return "# Agent Prompt\n\n## Response Format\n{...}"

    def test_init_with_valid_config_dir(self, config_dir: str) -> None:
        """Test successful initialization with valid config directory."""
        registry = AgentRegistry(config_dir)
        assert registry.config_dir == config_dir
        assert isinstance(registry.agents, dict)
        assert set(registry.agents.keys()) == {'core', 'estimation'}

    def test_load_valid_core_config(self, config_dir: str, mock_prompt_content: str) -> None:
        """Test loading valid core agent configuration."""
        with patch('builtins.open', mock_open(read_data=VALID_CORE_CONFIG)):
            with patch('os.path.exists', return_value=True):
                with patch('builtins.open', mock_open(read_data=mock_prompt_content)):
                    registry = AgentRegistry(config_dir)
                    assert 'agile_expert' in registry.agents['core']
                    agent = registry.agents['core']['agile_expert']
                    assert agent['name'] == "Agile Expert"
                    assert agent['model'] == "gpt-4-turbo-preview"

    def test_load_valid_estimation_config(self, config_dir: str, mock_prompt_content: str) -> None:
        """Test loading valid estimation agent configuration."""
        with patch('builtins.open', mock_open(read_data=VALID_ESTIMATION_CONFIG)):
            with patch('os.path.exists', return_value=True):
                with patch('builtins.open', mock_open(read_data=mock_prompt_content)):
                    registry = AgentRegistry(config_dir)
                    assert 'backend_dev' in registry.agents['estimation']
                    agent = registry.agents['estimation']['backend_dev']
                    assert agent['role'] == "backend_developer"
                    assert agent['expertise_level'] == "senior"

    def test_invalid_config_missing_fields(self, config_dir: str) -> None:
        """Test handling of invalid configuration with missing required fields."""
        with patch('builtins.open', mock_open(read_data=INVALID_CONFIG)):
            with pytest.raises(ValueError) as exc_info:
                registry = AgentRegistry(config_dir)
            assert "missing required fields" in str(exc_info.value)

    def test_get_agent_valid(self, config_dir: str, mock_prompt_content: str) -> None:
        """Test retrieving a valid agent configuration."""
        with patch('builtins.open', mock_open(read_data=VALID_CORE_CONFIG)):
            with patch('os.path.exists', return_value=True):
                with patch('builtins.open', mock_open(read_data=mock_prompt_content)):
                    registry = AgentRegistry(config_dir)
                    agent = registry.get_agent('core', 'agile_expert')
                    assert agent is not None
                    assert agent['name'] == "Agile Expert"

    def test_get_agent_invalid(self, config_dir: str) -> None:
        """Test retrieving an invalid agent configuration."""
        registry = AgentRegistry(config_dir)
        agent = registry.get_agent('core', 'nonexistent')
        assert agent is None

    def test_get_estimation_team(self, config_dir: str, mock_prompt_content: str) -> None:
        """Test retrieving all estimation team members."""
        with patch('builtins.open', mock_open(read_data=VALID_ESTIMATION_CONFIG)):
            with patch('os.path.exists', return_value=True):
                with patch('builtins.open', mock_open(read_data=mock_prompt_content)):
                    registry = AgentRegistry(config_dir)
                    team = registry.get_estimation_team()
                    assert isinstance(team, list)
                    assert len(team) == 1
                    assert team[0]['role'] == "backend_developer"

    def test_get_core_agents(self, config_dir: str, mock_prompt_content: str) -> None:
        """Test retrieving all core agents."""
        with patch('builtins.open', mock_open(read_data=VALID_CORE_CONFIG)):
            with patch('os.path.exists', return_value=True):
                with patch('builtins.open', mock_open(read_data=mock_prompt_content)):
                    registry = AgentRegistry(config_dir)
                    agents = registry.get_core_agents()
                    assert isinstance(agents, list)
                    assert len(agents) == 1
                    assert agents[0]['name'] == "Agile Expert" 