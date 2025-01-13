output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = module.api_gateway.api_endpoint
}

output "monitoring_dashboard_name" {
  description = "Name of the CloudWatch monitoring dashboard"
  value       = module.queues.monitoring_dashboard_name
}

output "stories_table_name" {
  description = "Name of the stories DynamoDB table"
  value       = module.dynamodb.stories_table_name
}

output "estimations_table_name" {
  description = "Name of the estimations DynamoDB table"
  value       = module.dynamodb.estimations_table_name
}

output "analysis_queue_url" {
  description = "URL of the story analysis queue"
  value       = module.queues.analysis_queue_url
}

output "estimation_queue_url" {
  description = "URL of the story estimation queue"
  value       = module.queues.estimation_queue_url
}

output "lambda_function_names" {
  description = "Names of the Lambda functions"
  value = {
    analyze_story  = module.lambda_functions.analyze_story_lambda_name
    estimate_story = module.lambda_functions.estimate_story_lambda_name
    get_status     = module.lambda_functions.get_status_lambda_name
  }
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = module.dynamodb.table_name
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table"
  value       = module.dynamodb.table_arn
} 