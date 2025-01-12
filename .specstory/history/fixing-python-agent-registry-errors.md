## SpecStory

## Fixing Python Agent Registry Errors (1/12/2025, 1:50:47 PM)

_**User**_

error

---

_**Assistant**_

The tests are failing because the mocking approach isn't working correctly. Let's fix both the registry implementation and the tests.

1. First, let's update the `AgentRegistry` class:

```python:backend/services/analysis/agents/registry.py
from pathlib import Path
from typing import Dict, Optional
import yaml
from pydantic import BaseModel


class AgentConfig(BaseModel):
    name: str
    description: str
    prompt_path: str
    model: str
    temperature: float


class AgentRegistry:
    def __init__(self, registry_path: Optional[Path] = None):
        self._agents: Dict[str, AgentConfig] = {}
        self._registry_path = registry_path
        self._load_registry()
    
    def _get_registry_path(self) -> Path:
        """Get path to registry.yaml file"""
        if self._registry_path:
            return self._registry_path
        return Path(__file__).parent / "config" / "registry.yaml"
    
    def _load_registry(self) -> None:
        """Load agent configurations from registry.yaml"""
        try:
            with open(self._get_registry_path(), 'r') as file:
                data = yaml.safe_load(file)
                if not data or 'agents' not in data:
                    raise RuntimeError("Invalid registry format")
                self._agents = {
                    agent_id: AgentConfig(**config)
                    for agent_id, config in data['agents'].items()
                }
        except yaml.YAMLError:
            raise RuntimeError("Invalid YAML in registry file")
        except Exception as e:
            raise RuntimeError(f"Failed to load agent registry: {e}")
```

2. Then update the test file:

```python:backend/tests/services/analysis/agents/test_registry.py
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
```

The key changes are:
1. Added `registry_path` parameter to `AgentRegistry`
2. Removed monkey-patching in favor of dependency injection
3. Fixed YAML formatting in test fixture
4. Improved error handling in registry loading

Would you like me to:
1. Show the remaining test implementations?
2. Add more test cases?
3. Show how to set up the actual registry configuration?

---



---

