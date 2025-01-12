output "analysis_queue_url" {
  description = "URL of the story analysis queue"
  value       = aws_sqs_queue.story_analysis.url
}

output "analysis_queue_arn" {
  description = "ARN of the story analysis queue"
  value       = aws_sqs_queue.story_analysis.arn
}

output "analysis_dlq_url" {
  description = "URL of the story analysis dead letter queue"
  value       = aws_sqs_queue.story_analysis_dlq.url
}

output "analysis_dlq_arn" {
  description = "ARN of the story analysis dead letter queue"
  value       = aws_sqs_queue.story_analysis_dlq.arn
}

output "estimation_queue_url" {
  description = "URL of the story estimation queue"
  value       = aws_sqs_queue.story_estimation.url
}

output "estimation_queue_arn" {
  description = "ARN of the story estimation queue"
  value       = aws_sqs_queue.story_estimation.arn
}

output "estimation_dlq_url" {
  description = "URL of the story estimation dead letter queue"
  value       = aws_sqs_queue.story_estimation_dlq.url
}

output "estimation_dlq_arn" {
  description = "ARN of the story estimation dead letter queue"
  value       = aws_sqs_queue.story_estimation_dlq.arn
}

output "sqs_policy_arn" {
  description = "ARN of the SQS access IAM policy"
  value       = aws_iam_policy.sqs_access.arn
}

output "monitoring_dashboard_name" {
  description = "Name of the CloudWatch monitoring dashboard"
  value       = aws_cloudwatch_dashboard.agile_stories.dashboard_name
} 