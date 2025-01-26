# API Gateway
output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = module.agile_stories.api_endpoint
}

# DynamoDB
output "stories_table_name" {
  description = "Name of the DynamoDB stories table"
  value       = module.agile_stories.stories_table_name
}

output "stories_table_arn" {
  description = "ARN of the DynamoDB stories table"
  value       = module.agile_stories.stories_table_arn
}

# SQS
output "analysis_queue_url" {
  description = "URL of the SQS analysis queue"
  value       = module.agile_stories.analysis_queue_url
}

output "estimation_queue_url" {
  description = "URL of the SQS estimation queue"
  value       = module.agile_stories.estimation_queue_url
}

# Lambda Functions
output "lambda_function_names" {
  description = "Names of all Lambda functions"
  value       = module.agile_stories.lambda_function_names
}

# Individual Lambda Names
output "analyze_story_lambda_name" {
  description = "Name of the analyze story Lambda function"
  value       = module.agile_stories.analyze_story_lambda_name
}

output "analyze_story_worker_lambda_name" {
  description = "Name of the analyze story worker Lambda function"
  value       = module.agile_stories.analyze_story_worker_lambda_name
}

output "team_estimate_lambda_name" {
  description = "Name of the team estimate Lambda function"
  value       = module.agile_stories.team_estimate_lambda_name
}

output "team_estimate_worker_lambda_name" {
  description = "Name of the team estimate worker Lambda function"
  value       = module.agile_stories.team_estimate_worker_lambda_name
}

output "technical_review_lambda_name" {
  description = "Name of the technical review Lambda function"
  value       = module.agile_stories.technical_review_lambda_name
}

output "technical_review_worker_lambda_name" {
  description = "Name of the technical review worker Lambda function"
  value       = module.agile_stories.technical_review_worker_lambda_name
}

output "get_status_lambda_name" {
  description = "Name of the get status Lambda function"
  value       = module.agile_stories.get_status_lambda_name
}

# Lambda ARNs
output "analyze_story_lambda_arn" {
  description = "ARN of the analyze story Lambda function"
  value       = module.agile_stories.analyze_story_lambda_arn
}

output "team_estimate_lambda_arn" {
  description = "ARN of the team estimate Lambda function"
  value       = module.agile_stories.team_estimate_lambda_arn
}

output "technical_review_lambda_arn" {
  description = "ARN of the technical review Lambda function"
  value       = module.agile_stories.technical_review_lambda_arn
}

output "get_status_lambda_arn" {
  description = "ARN of the get status Lambda function"
  value       = module.agile_stories.get_status_lambda_arn
}

output "step_functions_workflow_arn" {
  description = "ARN of the Story Refinement Step Functions workflow"
  value       = module.step_functions.workflow_arn
}

output "cognito_user_pool_id" {
  value = module.agile_stories.cognito_user_pool_id
}

output "cognito_user_pool_client_id" {
  value = module.agile_stories.cognito_user_pool_client_id
}

output "cognito_identity_pool_id" {
  value = module.agile_stories.cognito_identity_pool_id
} 