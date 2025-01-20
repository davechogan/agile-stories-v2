# API Gateway v2 (HTTP API)
resource "aws_apigatewayv2_api" "main" {
  name          = "${var.environment}-agile-stories-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = [for origin in var.domain_aliases : "https://${origin}"]
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers = ["Content-Type", "Authorization"]
    max_age      = 300
  }

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# Story Analysis Integration
resource "aws_apigatewayv2_integration" "analyze_story" {
  api_id                 = aws_apigatewayv2_api.main.id
  integration_type       = "AWS_PROXY"
  integration_method     = "POST"
  integration_uri        = var.analyze_story_lambda_arn
  description           = "Integration for story analysis"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "analyze_story" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "POST /stories/analyze"
  target    = "integrations/${aws_apigatewayv2_integration.analyze_story.id}"
}

# Team Estimation Integration
resource "aws_apigatewayv2_integration" "team_estimate" {
  api_id                 = aws_apigatewayv2_api.main.id
  integration_type       = "AWS_PROXY"
  integration_method     = "POST"
  integration_uri        = var.team_estimate_lambda_arn
  description           = "Integration for story estimation"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "team_estimate" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "POST /stories/estimate"
  target    = "integrations/${aws_apigatewayv2_integration.team_estimate.id}"
}

# Get Estimation Status Integration
resource "aws_apigatewayv2_integration" "get_estimation_status" {
  api_id                 = aws_apigatewayv2_api.main.id
  integration_type       = "AWS_PROXY"
  integration_method     = "POST"
  integration_uri        = var.get_status_lambda_arn
  description           = "Integration for getting estimation status"
  payload_format_version = "2.0"
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

resource "aws_lambda_permission" "team_estimate" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = var.team_estimate_lambda_name
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

# API Stage
resource "aws_apigatewayv2_stage" "main" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = var.environment
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_logs.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      routeKey       = "$context.routeKey"
      status         = "$context.status"
      protocol       = "$context.protocol"
      responseTime   = "$context.responseLatency"
      responseLength = "$context.responseLength"
    })
  }

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "api_logs" {
  name              = "/aws/apigateway/${var.environment}-agile-stories-api"
  retention_in_days = var.log_retention_days

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# VPC Link for private integration
resource "aws_apigatewayv2_vpc_link" "main" {
  name               = "${var.environment}-agile-stories-vpc-link"
  security_group_ids = [aws_security_group.vpc_link.id]
  subnet_ids         = var.subnet_ids

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# Security Group for VPC Link
resource "aws_security_group" "vpc_link" {
  name        = "${var.environment}-agile-stories-vpc-link"
  description = "Security group for API Gateway VPC Link"
  vpc_id      = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
} 