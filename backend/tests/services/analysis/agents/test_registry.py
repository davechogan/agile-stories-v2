import pytest
from pathlib import Path
from services.analysis.agents.registry import AgentRegistry, AgentConfig

class TestAgentRegistry:
    @pytest.fixture
    def valid_registry_yaml(self):
        return """
agents:
  test_agent:
    name: "Test Agent"
    description: "Agent for testing"
    prompt_path: "prompts/test_agent/prompt.md"
    model: "gpt-4-turbo-preview"
    temperature: 0.7
  another_agent:
    name: "Another Agent"
    description: "Another test agent"
    prompt_path: "prompts/another_agent/prompt.md"
    model: "gpt-4-turbo-preview"
    temperature: 0.5
"""

    def test_load_registry(self, tmp_path, valid_registry_yaml):
        # Create a temporary registry file
        registry_file = tmp_path / "registry.yaml"
        registry_file.write_text(valid_registry_yaml)
        
        # Create registry with test file
        registry = AgentRegistry(registry_path=registry_file)
        agents = registry.list_agents()
        
        assert len(agents) == 2
        assert "test_agent" in agents
        assert "another_agent" in agents
        
        test_agent = agents["test_agent"]
        assert test_agent.name == "Test Agent"
        assert test_agent.temperature == 0.7

    def test_invalid_registry_file(self, tmp_path):
        registry_file = tmp_path / "registry.yaml"
        registry_file.write_text("invalid: yaml: :")
        
        with pytest.raises(RuntimeError):
            AgentRegistry(registry_path=registry_file)
            