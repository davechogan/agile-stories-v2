import boto3
from botocore.exceptions import ClientError
from openai import OpenAI

def get_secret():
    secret_name = "openai_key"  # The name you used in AWS Secrets Manager
    region_name = "us-east-1"   # Your AWS region

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

def lambda_handler(event, context):
    # Get OpenAI API key from Secrets Manager
    openai_api_key = get_secret()
    
    # Initialize OpenAI client with the secret
    client = OpenAI(api_key=openai_api_key)
    
    # Your existing Lambda logic here
    return {
        'statusCode': 200,
        'body': 'Estimation placeholder'
    }
