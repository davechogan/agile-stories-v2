# Function Names
output "analyze_story_lambda_name" {
  description = "Name of the analyze story Lambda function"
  value       = aws_lambda_function.analyze_story.function_name
}

output "analyze_story_worker_lambda_name" {
  description = "Name of the analyze story worker Lambda function"
  value       = aws_lambda_function.analyze_story_worker.function_name
}

output "team_estimate_lambda_name" {
  description = "Name of the team estimate Lambda function"
  value       = aws_lambda_function.team_estimate.function_name
}

output "team_estimate_worker_lambda_name" {
  description = "Name of the team estimate worker Lambda function"
  value       = aws_lambda_function.team_estimate_worker.function_name
}

output "technical_review_lambda_name" {
  description = "Name of the technical review Lambda function"
  value       = aws_lambda_function.technical_review.function_name
}

output "technical_review_worker_lambda_name" {
  description = "Name of the technical review worker Lambda function"
  value       = aws_lambda_function.technical_review_worker.function_name
}

output "get_status_lambda_name" {
  description = "Name of the get status Lambda function"
  value       = aws_lambda_function.get_status.function_name
}

# Function ARNs
output "analyze_story_lambda_arn" {
  description = "ARN of the analyze story Lambda function"
  value       = aws_lambda_function.analyze_story.arn
}

output "analyze_story_worker_lambda_arn" {
  description = "ARN of the analyze story worker Lambda function"
  value       = aws_lambda_function.analyze_story_worker.arn
}

output "team_estimate_lambda_arn" {
  description = "ARN of the team estimate Lambda function"
  value       = aws_lambda_function.team_estimate.arn
}

output "team_estimate_worker_lambda_arn" {
  description = "ARN of the team estimate worker Lambda function"
  value       = aws_lambda_function.team_estimate_worker.arn
}

output "technical_review_lambda_arn" {
  description = "ARN of the technical review Lambda function"
  value       = aws_lambda_function.technical_review.arn
}

output "technical_review_worker_lambda_arn" {
  description = "ARN of the technical review worker Lambda function"
  value       = aws_lambda_function.technical_review_worker.arn
}

output "get_status_lambda_arn" {
  description = "ARN of the get status Lambda function"
  value       = aws_lambda_function.get_status.arn
}

output "story_state_handler_lambda_arn" {
  value = aws_lambda_function.story_state_handler.arn
}

# Combined list of function names
output "lambda_function_names" {
  description = "List of all Lambda function names"
  value = [
    aws_lambda_function.analyze_story.function_name,
    aws_lambda_function.analyze_story_worker.function_name,
    aws_lambda_function.team_estimate.function_name,
    aws_lambda_function.team_estimate_worker.function_name,
    aws_lambda_function.technical_review.function_name,
    aws_lambda_function.technical_review_worker.function_name,
    aws_lambda_function.get_status.function_name
  ]
}

# New outputs for DynamoDB configurations
output "lambda_dynamodb_policy_arn" {
  description = "ARN of the DynamoDB access policy"
  value       = aws_iam_role_policy.dynamodb_access.id
}

output "lambda_environment_variables" {
  description = "Common environment variables for Lambda functions"
  value       = local.lambda_environment_variables
}

# Note: Sensitive information should be marked as sensitive
output "lambda_role_arn" {
  description = "ARN of the IAM role used by Lambda functions"
  value       = aws_iam_role.lambda_role.arn
} 