## Updated outputs.tf for the DynamoDB module
output "stories_table_name" {
  description = "Name of the stories table"
  value       = aws_dynamodb_table.agile_stories.name
}

output "stories_table_arn" {
  description = "ARN of the stories table"
  value       = aws_dynamodb_table.agile_stories.arn
}

output "estimations_table_name" {
  description = "Name of the estimations table"
  value       = aws_dynamodb_table.estimations.name
}

output "estimations_table_arn" {
  description = "ARN of the estimations table"
  value       = aws_dynamodb_table.estimations.arn
}

output "locks_table_name" {
  description = "Name of the terraform locks table"
  value       = aws_dynamodb_table.terraform_locks.name
}

output "locks_table_arn" {
  description = "ARN of the terraform locks table"
  value       = aws_dynamodb_table.terraform_locks.arn
}

output "dynamodb_policy_arn" {
  description = "ARN of the DynamoDB access IAM policy"
  value       = aws_iam_policy.dynamodb_access.arn
}

output "terraform_locks_table_arn" {
  description = "ARN of the terraform locks table"
  value       = aws_dynamodb_table.terraform_locks.arn
}







