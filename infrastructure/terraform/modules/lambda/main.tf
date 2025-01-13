# IAM role for Lambda functions
resource "aws_iam_role" "lambda_role" {
  name = "${var.environment}-agile-stories-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# Lambda basic execution policy
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role.name
}

# Lambda VPC execution policy
resource "aws_iam_role_policy_attachment" "lambda_vpc" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
  role       = aws_iam_role.lambda_role.name
}

# Attach additional policies
resource "aws_iam_role_policy_attachment" "additional_policies" {
  count = length(var.additional_policy_arns)

  role       = aws_iam_role.lambda_role.name
  policy_arn = var.additional_policy_arns[count.index]
}

# Security Group for Lambda functions
resource "aws_security_group" "lambda" {
  name        = "${var.environment}-agile-stories-lambda"
  description = "Security group for Agile Stories Lambda functions"
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

# Story Analysis Lambda
resource "aws_lambda_function" "analyze_story" {
  filename      = var.analyze_story_package_path
  function_name = "${var.environment}-agile-stories-analyze"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.11"
  timeout       = 30
  memory_size   = 256

  environment {
    variables = {
      ENVIRONMENT    = var.environment
      OPENAI_API_KEY = var.openai_api_key
    }
  }

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# Story Estimation Lambda
resource "aws_lambda_function" "estimate_story" {
  filename      = var.estimate_story_package_path
  function_name = "${var.environment}-agile-stories-estimate"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.11"
  timeout       = 30
  memory_size   = 256

  environment {
    variables = {
      ENVIRONMENT    = var.environment
      OPENAI_API_KEY = var.openai_api_key
    }
  }

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# Get Estimation Status Lambda
resource "aws_lambda_function" "get_status" {
  filename      = var.get_status_package_path
  function_name = "${var.environment}-agile-stories-status"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.11"
  timeout       = 10
  memory_size   = 128

  environment {
    variables = {
      ENVIRONMENT = var.environment
    }
  }

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "analyze_story" {
  name              = "/aws/lambda/${aws_lambda_function.analyze_story.function_name}"
  retention_in_days = var.log_retention_days
}

resource "aws_cloudwatch_log_group" "estimate_story" {
  name              = "/aws/lambda/${aws_lambda_function.estimate_story.function_name}"
  retention_in_days = var.log_retention_days
}

resource "aws_cloudwatch_log_group" "get_status" {
  name              = "/aws/lambda/${aws_lambda_function.get_status.function_name}"
  retention_in_days = var.log_retention_days
} 