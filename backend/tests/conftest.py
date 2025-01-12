import pytest
from pathlib import Path

@pytest.fixture
def test_registry_yaml():
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

@pytest.fixture
def test_prompt():
    return "This is a test prompt template"
