# IAM Role for Step Functions
resource "aws_iam_role" "step_function_role" {
  name = "${var.name_prefix}-StepFunctionsRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "states.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# IAM Policy
resource "aws_iam_policy" "step_function_policy" {
  name = "${var.name_prefix}-StepFunctionsPolicy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunction"
        ]
        Resource = var.lambda_arns
      }
    ]
  })
}

# Policy Attachment
resource "aws_iam_role_policy_attachment" "policy_attachment" {
  role       = aws_iam_role.step_function_role.name
  policy_arn = aws_iam_policy.step_function_policy.arn
}

# Step Functions State Machine
resource "aws_sfn_state_machine" "state_machine" {
  name     = "${var.name_prefix}-StoryRefinementWorkflow"
  role_arn = aws_iam_role.step_function_role.arn

  definition = var.workflow_definition
}

# Add SSM Parameter for Step Functions ARN
resource "aws_ssm_parameter" "step_functions_arn" {
  name  = "/${var.environment}/step-functions/workflow-arn"
  type  = "String"
  value = aws_sfn_state_machine.state_machine.arn

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# IAM role for Step Functions to manage SSM parameters
resource "aws_iam_role_policy" "step_functions_ssm" {
  name = "${var.name_prefix}-step-functions-ssm"
  role = aws_iam_role.step_function_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:PutParameter",
          "ssm:GetParameter",
          "ssm:DeleteParameter"
        ]
        Resource = "arn:aws:ssm:*:*:parameter/${var.environment}/step-functions/*"
      }
    ]
  })
}

# Add DynamoDB policy
resource "aws_iam_role_policy" "step_functions_dynamodb" {
  name = "${var.name_prefix}-StepFunctionsDynamoDBPolicy"
  role = aws_iam_role.step_function_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:Query"
        ]
        Resource = [
          "arn:aws:dynamodb:us-east-1:${var.account_id}:table/${var.environment}-agile-stories"
        ]
      }
    ]
  })
}

# Add Lambda policy
resource "aws_iam_role_policy" "step_functions_lambda" {
  name = "${var.name_prefix}-StepFunctionsLambdaPolicy"
  role = aws_iam_role.step_function_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunction"
        ]
        Resource = ["*"]
      }
    ]
  })
}
