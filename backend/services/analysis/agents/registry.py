import os
import yaml
from typing import Dict, List, Optional, Literal

AgentType = Literal['core', 'estimation']

class AgentRegistry:
    """
    Registry for managing and validating AI agents and their configurations.

    This class handles the loading, validation, and access of agent configurations
    for both core analysis agents (Agile Expert, Senior Dev) and estimation team
    members. It ensures all agents have valid configurations and prompts.

    The registry supports two types of agents:
    1. Core Agents: Handle initial story analysis and improvements
    2. Estimation Agents: Participate in story estimation as team members

    Attributes:
        config_dir (str): Directory containing agent configuration files
        agents (Dict[AgentType, Dict]): Loaded and validated agent configurations
    """

    def __init__(self, config_dir: str):
        """
        Initialize the AgentRegistry.

        Args:
            config_dir (str): Path to the directory containing agent configuration files.
                            Expected to contain 'agents.yaml' and 'estimation_agents.yaml'
        
        Raises:
            ValueError: If the config directory doesn't exist or required files are missing
        """
        self.config_dir = config_dir
        self.agents: Dict[AgentType, Dict] = {
            'core': {},
            'estimation': {}
        }
        self._load_agents()

    def _load_agents(self) -> None:
        """
        Load both core and estimation agents from their respective config files.

        This method reads the YAML configuration files and validates each agent's
        configuration and associated prompt files.

        Raises:
            ValueError: If any configuration is invalid or required files are missing
        """
        config_files = {
            'core': 'agents.yaml',
            'estimation': 'estimation_agents.yaml'
        }

        for agent_type, filename in config_files.items():
            config_path = os.path.join(self.config_dir, filename)
            if os.path.exists(config_path):
                self.agents[agent_type] = self._load_config(agent_type, config_path)

    def _load_config(self, agent_type: AgentType, config_path: str) -> dict:
        """
        Load and validate a specific agent configuration file.

        Args:
            agent_type (AgentType): Type of agents being loaded ('core' or 'estimation')
            config_path (str): Path to the configuration file

        Returns:
            dict: Validated agent configurations

        Raises:
            ValueError: If the configuration file is invalid or missing required fields
            yaml.YAMLError: If the configuration file contains invalid YAML
        """
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)

            if not config or 'agents' not in config:
                raise ValueError(f"Invalid config file for {agent_type}: 'agents' section is missing")

            for name, agent in config['agents'].items():
                self._validate_agent_config(agent_type, name, agent)
                self._validate_prompt_file(agent_type, name, agent['prompt_file'])

            return config['agents']
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {agent_type} config file: {str(e)}")

    def _validate_agent_config(self, agent_type: AgentType, name: str, agent: dict) -> None:
        """
        Validate an individual agent's configuration.

        Args:
            agent_type (AgentType): Type of agent being validated
            name (str): Name of the agent
            agent (dict): Agent configuration to validate

        Raises:
            ValueError: If the configuration is missing required fields
        """
        required_fields = ['name', 'description', 'model', 'prompt_file']
        
        # Add estimation-specific required fields
        if agent_type == 'estimation':
            required_fields.extend(['role', 'expertise_level'])

        missing_fields = [
            field for field in required_fields 
            if field not in agent
        ]

        if missing_fields:
            raise ValueError(
                f"{agent_type.capitalize()} agent {name} is missing required fields: "
                f"{', '.join(missing_fields)}"
            )

    def _validate_prompt_file(self, agent_type: AgentType, name: str, prompt_file: str) -> None:
        """
        Validate that an agent's prompt file exists and contains required sections.

        Args:
            agent_type (AgentType): Type of agent the prompt belongs to
            name (str): Name of the agent
            prompt_file (str): Path to the prompt file relative to prompts directory

        Raises:
            ValueError: If the prompt file doesn't exist or is missing required sections
        """
        base_path = os.path.join(
            os.path.dirname(self.config_dir),
            "prompts",
            agent_type,
            prompt_file
        )

        if not os.path.exists(base_path):
            raise ValueError(
                f"Prompt file not found for {agent_type} agent {name}: {base_path}"
            )

        with open(base_path, 'r') as f:
            content = f.read().lower()
            if "response format" not in content:
                raise ValueError(
                    f"Prompt file for {agent_type} agent {name} is missing response format section"
                )

    def get_agent(self, agent_type: AgentType, name: str) -> Optional[dict]:
        """
        Retrieve a specific agent's configuration.

        Args:
            agent_type (AgentType): Type of agent to retrieve
            name (str): Name of the agent

        Returns:
            Optional[dict]: Agent configuration if found, None otherwise
        """
        return self.agents.get(agent_type, {}).get(name)

    def get_estimation_team(self) -> List[dict]:
        """
        Retrieve configurations for all estimation team members.

        Returns:
            List[dict]: List of configurations for all estimation agents
        """
        return list(self.agents['estimation'].values())

    def get_core_agents(self) -> List[dict]:
        """
        Retrieve configurations for all core analysis agents.

        Returns:
            List[dict]: List of configurations for all core agents
        """
        return list(self.agents['core'].values())

