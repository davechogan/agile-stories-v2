# API Gateway v2 (HTTP API)
resource "aws_apigatewayv2_api" "main" {
  name          = "${var.environment}-agile-stories-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = var.cors_allowed_origins
    allow_methods = ["GET", "POST", "PUT", "DELETE"]
    allow_headers = ["Content-Type", "Authorization"]
    max_age       = 300
  }

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
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