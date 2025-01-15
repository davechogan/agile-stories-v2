output "analysis_queue_url" {
  description = "URL of the analysis queue"
  value       = aws_sqs_queue.analysis.url
}

output "analysis_queue_arn" {
  description = "ARN of the analysis queue"
  value       = aws_sqs_queue.analysis_queue.arn
}

output "analysis_dlq_url" {
  description = "URL of the analysis DLQ"
  value       = aws_sqs_queue.analysis_dlq.url
}

output "analysis_dlq_arn" {
  description = "ARN of the analysis DLQ"
  value       = aws_sqs_queue.analysis_dlq.arn
}

output "estimation_queue_url" {
  description = "URL of the estimation queue"
  value       = aws_sqs_queue.story_estimation.url
}

output "estimation_queue_arn" {
  description = "ARN of the estimation queue"
  value       = aws_sqs_queue.story_estimation.arn
}

output "estimation_dlq_url" {
  description = "URL of the estimation DLQ"
  value       = aws_sqs_queue.story_estimation_dlq.url
}

output "estimation_dlq_arn" {
  description = "ARN of the estimation DLQ"
  value       = aws_sqs_queue.story_estimation_dlq.arn
}

output "sqs_policy_arn" {
  description = "ARN of the SQS access IAM policy"
  value       = aws_iam_policy.sqs_access.arn
} 