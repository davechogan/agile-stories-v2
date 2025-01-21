# Add this at the top of the file, after the variables
locals {
  lambda_environment_variables = {
    ENVIRONMENT = var.environment
  }
}

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
    variables = {
      DYNAMODB_TABLE  = var.dynamodb_table_name
      ENVIRONMENT     = var.environment
      ERROR_SNS_TOPIC = var.error_sns_topic_arn
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

# Story Analysis Worker Lambda
resource "aws_lambda_function" "analyze_story_worker" {
  filename      = var.analyze_story_worker_package_path
  function_name = "${var.environment}-agile-stories-analyze-worker"
  role          = aws_iam_role.lambda_role.arn
  handler       = "app.handler"
  runtime       = "python3.11"
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory_size

  environment {
    variables = merge(local.lambda_environment_variables, {
      DYNAMODB_TABLE  = var.dynamodb_table_name
      ERROR_SNS_TOPIC = var.error_sns_topic_arn
      OPENAI_API_KEY  = var.openai_api_key
    })
  }

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }
}

# Technical Review Lambda
resource "aws_lambda_function" "technical_review" {
  filename      = var.technical_review_package_path
  function_name = "${var.environment}-agile-stories-review"
  role          = aws_iam_role.lambda_role.arn
  handler       = "app.handler"
  runtime       = "python3.11"
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory_size

  environment {
    variables = merge(local.lambda_environment_variables, {
      DYNAMODB_TABLE  = var.dynamodb_table_name
      ERROR_SNS_TOPIC = var.error_sns_topic_arn
    })
  }

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }
}

# Technical Review Worker Lambda
resource "aws_lambda_function" "technical_review_worker" {
  filename      = var.technical_review_worker_package_path
  function_name = "${var.environment}-agile-stories-review-worker"
  role          = aws_iam_role.lambda_role.arn
  handler       = "app.handler"
  runtime       = "python3.11"
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory_size

  environment {
    variables = merge(local.lambda_environment_variables, {
      DYNAMODB_TABLE  = var.dynamodb_table_name
      ERROR_SNS_TOPIC = var.error_sns_topic_arn
      OPENAI_API_KEY  = var.openai_api_key
    })
  }

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }
}

# Team Estimate Lambda
resource "aws_lambda_function" "team_estimate" {
  filename      = var.team_estimate_package_path
  function_name = "${var.environment}-agile-stories-estimate"
  role          = aws_iam_role.lambda_role.arn
  handler       = "app.handler"
  runtime       = "python3.11"
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory_size

  environment {
    variables = merge(local.lambda_environment_variables, {
      DYNAMODB_TABLE  = var.dynamodb_table_name
      ERROR_SNS_TOPIC = var.error_sns_topic_arn
    })
  }

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }
}

# Team Estimate Worker Lambda
resource "aws_lambda_function" "team_estimate_worker" {
  filename      = var.team_estimate_worker_package_path
  function_name = "${var.environment}-agile-stories-estimate-worker"
  role          = aws_iam_role.lambda_role.arn
  handler       = "app.handler"
  runtime       = "python3.11"
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory_size

  environment {
    variables = merge(local.lambda_environment_variables, {
      DYNAMODB_TABLE  = var.dynamodb_table_name
      ERROR_SNS_TOPIC = var.error_sns_topic_arn
      OPENAI_API_KEY  = var.openai_api_key
    })
  }

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
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

# Story State Handler Lambda
resource "aws_lambda_function" "story_state_handler" {
  filename         = var.story_state_handler_package_path
  function_name    = "${var.environment}-agile-stories-story-state-handler"
  role            = aws_iam_role.lambda_role.arn
  handler         = "app.lambda_handler"
  source_code_hash = filebase64sha256(var.story_state_handler_package_path)
  runtime         = "python3.11"
  timeout         = 30
  memory_size     = 128

  environment {
    variables = {
      DYNAMODB_TABLE = "${var.environment}-agile-stories"
      ENVIRONMENT    = var.environment
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

# Workflow Signal Handler Lambda
resource "aws_lambda_function" "workflow_signal_handler" {
  filename         = var.workflow_signal_handler_package_path
  function_name    = "${var.environment}-agile-stories-workflow-signal-handler"
  role            = aws_iam_role.lambda_role.arn
  handler         = "app.lambda_handler"
  source_code_hash = filebase64sha256(var.workflow_signal_handler_package_path)
  runtime         = "python3.11"
  timeout         = 30
  memory_size     = 128

  environment {
    variables = {
      DYNAMODB_TABLE = "${var.environment}-agile-stories"
      ENVIRONMENT    = var.environment
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

resource "aws_cloudwatch_log_group" "story_state_handler" {
  name              = "/aws/lambda/${aws_lambda_function.story_state_handler.function_name}"
  retention_in_days = var.log_retention_days
}

resource "aws_cloudwatch_log_group" "workflow_signal_handler" {
  name              = "/aws/lambda/${aws_lambda_function.workflow_signal_handler.function_name}"
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

# New Lambda functions needed:
resource "aws_lambda_function" "error_handler" {
  filename      = var.error_handler_package_path
  function_name = "${var.function_name}-error-handler"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "nodejs18.x"
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory_size

  environment {
    variables = merge(local.lambda_environment_variables, {
      ERROR_SNS_TOPIC = var.error_sns_topic_arn
    })
  }
}

# Add Step Functions permissions to Lambda role
resource "aws_iam_role_policy" "lambda_step_functions" {
  name = "${var.environment}-lambda-step-functions"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "states:StartExecution",
          "states:SendTaskSuccess",
          "states:SendTaskFailure",
          "states:SendTaskHeartbeat",
          "states:GetActivityTask",
          "states:GetExecutionHistory",
          "states:ListActivities",
          "states:ListExecutions"
        ]
        Resource = [
          "arn:aws:states:${var.aws_region}:${var.account_id}:stateMachine:${var.environment}-StoryRefinementWorkflow",
          "arn:aws:states:${var.aws_region}:${var.account_id}:execution:${var.environment}-StoryRefinementWorkflow:*"
        ]
      }
    ]
  })
}

# Add SSM read permission to Lambda role
resource "aws_iam_role_policy" "lambda_ssm" {
  name = "${var.environment}-lambda-ssm-access"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter"
        ]
        Resource = "arn:aws:ssm:*:*:parameter/${var.environment}/step-functions/*"
      }
    ]
  })
}

# ... rest of the Lambda configurations using local.lambda_environment_variables ... 

resource "aws_iam_policy" "secrets_access" {
  name        = "${var.environment}-secrets-access-policy"
  description = "IAM policy for accessing secrets"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = [
          "arn:aws:secretsmanager:us-east-1:784902437693:secret:openai_key-uPA0lN"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "analyze_story_worker_secrets" {
  policy_arn = aws_iam_policy.secrets_access.arn
  role       = "dev-agile-stories-lambda-role"
}
