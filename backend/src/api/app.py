def lambda_handler(event, context):
    # Handle OPTIONS request for CORS
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'OPTIONS,POST',
                'Access-Control-Max-Age': '3600'
            },
            'body': ''
        }

    try:
        print("Received event:", event)  # Log incoming request
        
        # ... existing code ...

        print("Calling OpenAI...")  # Log before OpenAI call
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        print("OpenAI response received:", response)  # Log OpenAI response

        # ... rest of your code ...

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log any errors
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'OPTIONS,POST',
                'Access-Control-Max-Age': '3600'
            },
            'body': json.dumps({'error': str(e)})
        } 