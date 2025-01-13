import json
import os
import boto3
from botocore.exceptions import ClientError
from openai import OpenAI
from typing import Dict, Any

def get_secret():
    secret_name = "openai_key"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        return get_secret_value_response['SecretString']
    except ClientError as e:
        raise e

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for processing story analysis and estimation requests.

    This function serves as the entry point for all AI agents, processing stories
    through OpenAI's API based on specific agent configurations and prompts.

    Args:
        event (Dict[str, Any]): Lambda event containing:
            - story_data: The story to be analyzed
            - agent_config: Configuration for the specific agent
            - prompt_file: Path to the agent's prompt template
        context (Any): AWS Lambda context object

    Returns:
        Dict[str, Any]: Response containing either:
            - statusCode: 200 and processed results in body
            - statusCode: 500 and error details in body

    Raises:
        No exceptions are raised; all are caught and returned in the response
    """
    try:
        # Extract required data from the event
        story_data = event['story_data']
        agent_config = event['agent_config']
        prompt_file = event['prompt_file']

        # Initialize OpenAI client using secret
        openai_api_key = get_secret()
        client = OpenAI(api_key=openai_api_key)

        # Load the appropriate prompt template
        prompt_template = load_prompt(prompt_file)

        # Prepare messages for OpenAI API
        messages = [
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": json.dumps(story_data, indent=2)}
        ]

        # Make API call to OpenAI
        response = client.chat.completions.create(
            model=agent_config['model'],
            messages=messages,
            temperature=agent_config.get('temperature', 0.7)
        )

        # Parse and validate response
        result = json.loads(response.choices[0].message.content)

        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }

    except Exception as e:
        # Return any errors in a structured format
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 