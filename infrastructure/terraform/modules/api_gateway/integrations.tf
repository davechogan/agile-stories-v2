# Story Analysis Integration
resource "aws_apigatewayv2_integration" "analyze_story" {
  api_id                 = aws_apigatewayv2_api.main.id
  integration_type       = "AWS_PROXY"
  integration_uri        = var.analyze_story_lambda_arn
  payload_format_version = "2.0"
  description            = "Integration for story analysis"
}

resource "aws_apigatewayv2_route" "analyze_story" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "POST /stories/analyze"
  target    = "integrations/${aws_apigatewayv2_integration.analyze_story.id}"
}

# Story Estimation Integration
resource "aws_apigatewayv2_integration" "estimate_story" {
  api_id                 = aws_apigatewayv2_api.main.id
  integration_type       = "AWS_PROXY"
  integration_uri        = var.estimate_story_lambda_arn
  payload_format_version = "2.0"
  description            = "Integration for story estimation"
}

resource "aws_apigatewayv2_route" "estimate_story" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "POST /stories/estimate"
  target    = "integrations/${aws_apigatewayv2_integration.estimate_story.id}"
}

# Get Estimation Status Integration
resource "aws_apigatewayv2_integration" "get_estimation_status" {
  api_id                 = aws_apigatewayv2_api.main.id
  integration_type       = "AWS_PROXY"
  integration_uri        = var.get_status_lambda_arn
  payload_format_version = "2.0"
  description            = "Integration for getting estimation status"
}

resource "aws_apigatewayv2_route" "get_estimation_status" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "GET /stories/{storyId}/estimation"
  target    = "integrations/${aws_apigatewayv2_integration.get_estimation_status.id}"
}

# Lambda Permissions
resource "aws_lambda_permission" "analyze_story" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = var.analyze_story_lambda_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

resource "aws_lambda_permission" "estimate_story" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = var.estimate_story_lambda_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

resource "aws_lambda_permission" "get_estimation_status" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = var.get_status_lambda_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
} 