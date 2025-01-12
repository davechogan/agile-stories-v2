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
    
    def get_agent(self, agent_id: str) -> Optional[AgentConfig]:
        """Get agent configuration by ID"""
        return self._agents.get(agent_id)
    
    def list_agents(self) -> Dict[str, AgentConfig]:
        """List all available agents"""
        return self._agents.copy()
    
    def load_prompt(self, agent_id: str) -> str:
        """Load prompt template for specified agent"""
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Unknown agent: {agent_id}")
            
        prompt_path = Path(__file__).parent / agent.prompt_path
        
        try:
            with open(prompt_path, 'r') as file:
                return file.read()
        except Exception as e:
            raise RuntimeError(f"Failed to load prompt for {agent_id}: {e}")
    
    def _get_base_path(self) -> Path:
        """Get base path for prompt files"""
        return Path(__file__).parent

