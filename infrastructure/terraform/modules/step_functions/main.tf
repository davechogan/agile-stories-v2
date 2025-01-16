# IAM Role for Step Functions
resource "aws_iam_role" "step_function_role" {
  name = "${var.name_prefix}-StepFunctionsRole"

  assume_role_policy = jsonencode({
    Version : "2012-10-17",
    Statement : [
      {
        Effect : "Allow",
        Principal : {
          Service : "states.amazonaws.com"
        },
        Action : "sts:AssumeRole"
      }
    ]
  })
}

# IAM Policy for Step Functions to invoke Lambdas
resource "aws_iam_policy" "step_function_policy" {
  name = "${var.name_prefix}-StepFunctionsPolicy"
  policy = jsonencode({
    Version : "2012-10-17",
    Statement : [
      {
        Effect : "Allow",
        Action : [
          "lambda:InvokeFunction"
        ],
        Resource = var.lambda_arns
      }
    ]
  })
}

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
