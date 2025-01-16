import json

def handler(event, context):
    print("Error event received:", json.dumps(event))
    # Add custom error handling logic here
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Error handled successfully"})
    }
