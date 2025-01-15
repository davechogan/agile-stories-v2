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
  handler       = "app.handler"
  runtime       = "python3.11"
  timeout       = 30
  memory_size   = 256


  environment {
    variables = merge(local.lambda_environment_variables, {
      STEP_FUNCTION_ARN = aws_sfn_state_machine.story_analysis.arn
      ERROR_SNS_TOPIC = var.error_sns_topic_arn
    })
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
resource "aws_lambda_function" "team_estimate" {
  filename      = var.team_estimate_package_path
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

resource "aws_cloudwatch_log_group" "team_estimate" {
  name              = "/aws/lambda/${aws_lambda_function.team_estimate.function_name}"
  retention_in_days = var.log_retention_days
}

resource "aws_cloudwatch_log_group" "get_status" {
  name              = "/aws/lambda/${aws_lambda_function.get_status.function_name}"
  retention_in_days = var.log_retention_days
}

resource "aws_iam_role_policy" "dynamodb_access" {
  name = "${var.environment}-agile-stories-dynamodb-access"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:BatchGetItem",
          "dynamodb:BatchWriteItem"
        ]
        Resource = [
          var.dynamodb_table_arn,
          "${var.dynamodb_table_arn}/index/*"
        ]
      }
    ]
  })
}

# Add this to your IAM role policy
resource "aws_iam_role_policy" "secrets_manager_policy" {
  name = "${var.function_name}-secrets-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = "arn:aws:secretsmanager:${var.aws_region}:${var.account_id}:secret:openai_key*"
      }
    ]
  })
}

# Worker Lambda functions
resource "aws_lambda_function" "analyze_story_worker" {
  filename      = var.analyze_story_worker_package_path
  function_name = "${var.environment}-agile-stories-analyze-worker"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "nodejs18.x"
  memory_size   = var.lambda_memory_size
  timeout       = var.lambda_timeout

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      OPENAI_API_KEY = var.openai_api_key
    }
  }
}

resource "aws_lambda_function" "team_estimate_worker" {
  filename      = var.team_estimate_worker_package_path
  function_name = "${var.environment}-agile-stories-estimate-worker"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "nodejs18.x"
  memory_size   = var.lambda_memory_size
  timeout       = var.lambda_timeout

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      OPENAI_API_KEY = var.openai_api_key
    }
  }
}

resource "aws_lambda_function" "technical_review" {
  filename      = var.technical_review_package_path
  function_name = "${var.environment}-agile-stories-review"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "nodejs18.x"
  memory_size   = var.lambda_memory_size
  timeout       = var.lambda_timeout

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      OPENAI_API_KEY = var.openai_api_key
    }
  }
}

resource "aws_lambda_function" "technical_review_worker" {
  filename      = var.technical_review_worker_package_path
  function_name = "${var.environment}-agile-stories-review-worker"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "nodejs18.x"
  memory_size   = var.lambda_memory_size
  timeout       = var.lambda_timeout

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      OPENAI_API_KEY = var.openai_api_key
    }
  }
}

# Update environment variables
locals {
  lambda_environment_variables = {
    STORIES_TABLE     = var.stories_table_name
    ESTIMATIONS_TABLE = var.estimations_table_name
    TENANT_INDEX      = var.tenant_index_name
  }
}

# Update IAM policy
data "aws_iam_policy_document" "lambda_dynamodb_policy" {
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:UpdateItem",
      "dynamodb:DeleteItem",
      "dynamodb:Query",
      "dynamodb:Scan"
    ]
    resources = [
      var.stories_table_arn,
      "${var.stories_table_arn}/index/*",
      var.estimations_table_arn,
      "${var.estimations_table_arn}/index/*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "dynamodb:GetRecords",
      "dynamodb:GetShardIterator",
      "dynamodb:DescribeStream",
      "dynamodb:ListStreams"
    ]
    resources = [
      var.stories_table_stream_arn,
      var.estimations_table_stream_arn
    ]
  }
}

# Add the IAM policy for DynamoDB access
resource "aws_iam_policy" "dynamodb_access" {
  name        = "${var.environment}-lambda-dynamodb-access"
  description = "IAM policy for Lambda to access DynamoDB tables"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          var.stories_table_arn,
          "${var.stories_table_arn}/index/*",
          var.estimations_table_arn,
          "${var.estimations_table_arn}/index/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetRecords",
          "dynamodb:GetShardIterator",
          "dynamodb:DescribeStream",
          "dynamodb:ListStreams"
        ]
        Resource = [
          var.stories_table_stream_arn,
          var.estimations_table_stream_arn
        ]
      }
    ]
  })
}

# New Lambda functions needed:
resource "aws_lambda_function" "error_handler" {
  filename         = var.error_handler_package_path
  function_name    = "${var.function_name}-error-handler"
  role            = aws_iam_role.lambda_role.arn
  handler         = "index.handler"
  runtime         = "nodejs18.x"
  timeout         = var.lambda_timeout
  memory_size     = var.lambda_memory_size

  environment {
    variables = merge(local.lambda_environment_variables, {
      ERROR_SNS_TOPIC = aws_sns_topic.error_notifications.arn
    })
  }
}


# ... rest of the Lambda configurations using local.lambda_environment_variables ... 

resource "aws_lambda_function" "analyze_story" {
  # Other Lambda configurations...

  environment {
    variables = {
      STEP_FUNCTION_ARN = var.step_function_arn
    }
  }
}
