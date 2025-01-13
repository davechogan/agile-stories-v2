output "analysis_queue_url" {
  value       = aws_sqs_queue.analysis_queue.url
  description = "URL of the analysis queue"
}

output "analysis_queue_arn" {
  value       = aws_sqs_queue.analysis_queue.arn
  description = "ARN of the analysis queue"
}

output "analysis_dlq_url" {
  value       = aws_sqs_queue.analysis_dlq.url
  description = "URL of the analysis DLQ"
}

output "analysis_dlq_arn" {
  value       = aws_sqs_queue.analysis_dlq.arn
  description = "ARN of the analysis DLQ"
} 