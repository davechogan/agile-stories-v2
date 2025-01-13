resource "aws_api_gateway_rest_api" "agile_stories" {
  name = "dev-agile-stories-api"
}

resource "aws_api_gateway_resource" "stories" {
  rest_api_id = aws_api_gateway_rest_api.agile_stories.id
  parent_id   = aws_api_gateway_rest_api.agile_stories.root_resource_id
  path_part   = "stories"
}

# POST /stories/analyze endpoint
resource "aws_api_gateway_method" "analyze_story" {
  rest_api_id   = aws_api_gateway_rest_api.agile_stories.id
  resource_id   = aws_api_gateway_resource.stories.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "analyze_story" {
  rest_api_id = aws_api_gateway_rest_api.agile_stories.id
  resource_id = aws_api_gateway_resource.stories.id
  http_method = aws_api_gateway_method.analyze_story.http_method
  type        = "AWS_PROXY"
  uri         = aws_lambda_function.analyze_story.invoke_arn
}

# CORS Configuration
resource "aws_api_gateway_method" "stories_options" {
  rest_api_id   = aws_api_gateway_rest_api.agile_stories.id
  resource_id   = aws_api_gateway_resource.stories.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "stories_options" {
  rest_api_id = aws_api_gateway_rest_api.agile_stories.id
  resource_id = aws_api_gateway_resource.stories.id
  http_method = aws_api_gateway_method.stories_options.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "stories_options_200" {
  rest_api_id = aws_api_gateway_rest_api.agile_stories.id
  resource_id = aws_api_gateway_resource.stories.id
  http_method = aws_api_gateway_method.stories_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "stories_options_200" {
  rest_api_id = aws_api_gateway_rest_api.agile_stories.id
  resource_id = aws_api_gateway_resource.stories.id
  http_method = aws_api_gateway_method.stories_options.http_method
  status_code = aws_api_gateway_method_response.stories_options_200.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,POST,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'" # Will be updated to dev CloudFront domain
  }
} 