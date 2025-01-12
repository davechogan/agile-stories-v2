import os
import json
import boto3
from typing import Dict, Any, List
from botocore.exceptions import ClientError

class AgentProcessor:
    """
    Manages the processing of story analysis and estimation through AWS Lambda functions.
    
    This class handles the distribution of work to various AI agents (implemented as Lambda 
    functions) that analyze and estimate user stories. It supports both individual agent 
    processing and parallel team estimation.

    Attributes:
        registry (AgentRegistry): Registry containing agent configurations and prompts.
        lambda_client (boto3.client): AWS Lambda client for function invocation.
        region (str): AWS region for Lambda functions.
    """

    def __init__(self, registry: AgentRegistry):
        """
        Initialize the AgentProcessor.

        Args:
            registry (AgentRegistry): An instance of AgentRegistry containing agent configurations.
        """
        self.registry = registry
        self.lambda_client = boto3.client('lambda')
        self.region = os.getenv('AWS_REGION', 'us-east-1')

    async def process_with_agent(
        self, 
        agent_type: str, 
        agent_name: str, 
        story_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process a story with a specific agent through Lambda invocation.

        Args:
            agent_type (str): Type of agent ('core' or 'estimation').
            agent_name (str): Name of the specific agent to use.
            story_data (Dict[str, Any]): Story data to be processed.

        Returns:
            Dict[str, Any]: Processed results from the agent.

        Raises:
            ValueError: If the specified agent is not found.
            RuntimeError: If Lambda invocation fails.
        """
        # Retrieve agent configuration from registry
        agent = self.registry.get_agent(agent_type, agent_name)
        if not agent:
            raise ValueError(f"Agent {agent_name} not found in {agent_type}")

        # Construct Lambda function name based on agent type and name
        function_name = f"agile-stories-{agent_type}-{agent_name}"
        
        # Prepare payload for Lambda function
        payload = {
            "story_data": story_data,
            "agent_config": agent,
            "prompt_file": agent['prompt_file']
        }

        try:
            response = await self._invoke_lambda(function_name, payload)
            return self._parse_response(response)
        except Exception as e:
            raise RuntimeError(f"Error processing with {agent_name}: {str(e)}")

    async def process_team_estimation(
        self, 
        story_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Process story estimation with all team members in parallel.

        This method invokes all estimation agents concurrently to simulate a real-time
        planning poker session with the entire team.

        Args:
            story_data (Dict[str, Any]): Story data to be estimated.

        Returns:
            List[Dict[str, Any]]: List of estimation results from all team members.
        """
        # Get all estimation agents from registry
        estimation_agents = self.registry.get_estimation_team()
        
        # Create concurrent tasks for each agent
        tasks = [
            self.process_with_agent('estimation', agent['name'], story_data)
            for agent in estimation_agents
        ]
        
        # Execute all estimations in parallel
        return await asyncio.gather(*tasks)

    async def _invoke_lambda(
        self, 
        function_name: str, 
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Invoke an AWS Lambda function asynchronously.

        Args:
            function_name (str): Name of the Lambda function to invoke.
            payload (Dict[str, Any]): Data to send to the Lambda function.

        Returns:
            Dict[str, Any]: Response from the Lambda function.

        Raises:
            RuntimeError: If Lambda invocation fails.
        """
        try:
            response = await self.lambda_client.invoke_async(
                FunctionName=function_name,
                InvokeArgs=json.dumps(payload)
            )
            return json.loads(response['Payload'].read())
        except ClientError as e:
            raise RuntimeError(f"Lambda invocation failed: {str(e)}") 