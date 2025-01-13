output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = module.api_gateway.api_endpoint
}

output "stories_table_name" {
  description = "Name of the DynamoDB stories table"
  value       = module.dynamodb.stories_table_name
}

output "stories_table_arn" {
  description = "ARN of the DynamoDB stories table"
  value       = module.dynamodb.stories_table_arn
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
  description = "Names of the Lambda functions"
  value = [
    module.lambda.analyze_story_lambda_name,
    module.lambda.estimate_story_lambda_name,
    module.lambda.get_status_lambda_name
  ]
}

output "analyze_story_lambda_name" {
  description = "Name of the analyze story Lambda function"
  value       = module.lambda.analyze_story_lambda_name
}

output "estimate_story_lambda_name" {
  description = "Name of the estimate story Lambda function"
  value       = module.lambda.estimate_story_lambda_name
}

output "get_status_lambda_name" {
  description = "Name of the get status Lambda function"
  value       = module.lambda.get_status_lambda_name
}
