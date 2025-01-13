output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = module.agile_stories.api_endpoint
}

output "monitoring_dashboard_name" {
  description = "Name of the CloudWatch monitoring dashboard"
  value       = module.agile_stories.monitoring_dashboard_name
}

output "stories_table_name" {
  description = "Name of the stories DynamoDB table"
  value       = module.agile_stories.stories_table_name
}

output "analysis_queue_url" {
  description = "URL of the story analysis queue"
  value       = module.agile_stories.analysis_queue_url
}

output "estimation_queue_url" {
  description = "URL of the story estimation queue"
  value       = module.agile_stories.estimation_queue_url
}

output "lambda_function_names" {
  description = "Names of the Lambda functions"
  value       = module.agile_stories.lambda_function_names
} 