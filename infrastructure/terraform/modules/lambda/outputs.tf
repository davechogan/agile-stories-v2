output "analyze_story_lambda_arn" {
  description = "ARN of the analyze story Lambda function"
  value       = aws_lambda_function.analyze_story.arn
}

output "estimate_story_lambda_arn" {
  description = "ARN of the estimate story Lambda function"
  value       = aws_lambda_function.estimate_story.arn
}

output "get_status_lambda_arn" {
  description = "ARN of the get status Lambda function"
  value       = aws_lambda_function.get_status.arn
}

output "analyze_story_lambda_name" {
  description = "Name of the analyze story Lambda function"
  value       = aws_lambda_function.analyze_story.function_name
}

output "estimate_story_lambda_name" {
  description = "Name of the estimate story Lambda function"
  value       = aws_lambda_function.estimate_story.function_name
}

output "get_status_lambda_name" {
  description = "Name of the get status Lambda function"
  value       = aws_lambda_function.get_status.function_name
}

output "lambda_role_arn" {
  description = "ARN of the Lambda IAM role"
  value       = aws_iam_role.lambda_role.arn
}

output "lambda_security_group_id" {
  description = "ID of the Lambda security group"
  value       = aws_security_group.lambda.id
} 