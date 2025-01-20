output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = module.api_gateway.api_endpoint
}

output "analysis_queue_url" {
  description = "URL of the SQS analysis queue"
  value       = module.sqs.analysis_queue_url
}

output "estimation_queue_url" {
  description = "URL of the SQS estimation queue"
  value       = module.sqs.estimation_queue_url
}

output "lambda_function_names" {
  description = "Names of all Lambda functions"
  value = [
    module.lambda.analyze_story_lambda_name,
    module.lambda.analyze_story_worker_lambda_name,
    module.lambda.team_estimate_lambda_name,
    module.lambda.team_estimate_worker_lambda_name,
    module.lambda.technical_review_lambda_name,
    module.lambda.technical_review_worker_lambda_name,
    module.lambda.get_status_lambda_name
  ]
}

# Individual Lambda function names
output "analyze_story_lambda_name" {
  description = "Name of the analyze story Lambda function"
  value       = module.lambda.analyze_story_lambda_name
}

output "analyze_story_worker_lambda_name" {
  description = "Name of the analyze story worker Lambda function"
  value       = module.lambda.analyze_story_worker_lambda_name
}

output "team_estimate_lambda_name" {
  description = "Name of the team estimate Lambda function"
  value       = module.lambda.team_estimate_lambda_name
}

output "team_estimate_worker_lambda_name" {
  description = "Name of the team estimate worker Lambda function"
  value       = module.lambda.team_estimate_worker_lambda_name
}

output "technical_review_lambda_name" {
  description = "Name of the technical review Lambda function"
  value       = module.lambda.technical_review_lambda_name
}

output "technical_review_worker_lambda_name" {
  description = "Name of the technical review worker Lambda function"
  value       = module.lambda.technical_review_worker_lambda_name
}

output "get_status_lambda_name" {
  description = "Name of the get status Lambda function"
  value       = module.lambda.get_status_lambda_name
}

# Lambda ARNs
output "analyze_story_lambda_arn" {
  description = "ARN of the analyze story Lambda function"
  value       = module.lambda.analyze_story_lambda_arn
}

output "analyze_story_worker_lambda_arn" {
  description = "ARN of the analyze story worker Lambda function"
  value       = module.lambda.analyze_story_worker_lambda_arn
}

output "team_estimate_lambda_arn" {
  description = "ARN of the team estimate Lambda function"
  value       = module.lambda.team_estimate_lambda_arn
}

output "team_estimate_worker_lambda_arn" {
  description = "ARN of the team estimate worker Lambda function"
  value       = module.lambda.team_estimate_worker_lambda_arn
}

output "technical_review_lambda_arn" {
  description = "ARN of the technical review Lambda function"
  value       = module.lambda.technical_review_lambda_arn
}

output "technical_review_worker_lambda_arn" {
  description = "ARN of the technical review worker Lambda function"
  value       = module.lambda.technical_review_worker_lambda_arn
}

output "get_status_lambda_arn" {
  description = "ARN of the get status Lambda function"
  value       = module.lambda.get_status_lambda_arn
}

output "workflow_signal_handler_lambda_arn" {
  description = "ARN of the workflow signal handler Lambda function"
  value       = module.lambda.workflow_signal_handler_lambda_arn
}

output "stories_table_name" {
  description = "Name of the stories DynamoDB table"
  value       = module.dynamodb.stories_table_name
}

output "stories_table_arn" {
  description = "ARN of the stories DynamoDB table"
  value       = module.dynamodb.stories_table_arn
}

output "stories_table_stream_arn" {
  description = "Stream ARN of the stories DynamoDB table"
  value       = module.dynamodb.stories_table_stream_arn
}