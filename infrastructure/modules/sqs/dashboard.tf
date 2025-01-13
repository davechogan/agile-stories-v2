resource "aws_cloudwatch_dashboard" "sqs_dashboard" {
  dashboard_name = "${var.prefix}-sqs-metrics"

  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/SQS", "ApproximateAgeOfOldestMessage", "QueueName", aws_sqs_queue.analysis_queue.name],
            ["AWS/SQS", "NumberOfMessagesReceived", "QueueName", aws_sqs_queue.analysis_queue.name],
            ["AWS/SQS", "NumberOfMessagesDeleted", "QueueName", aws_sqs_queue.analysis_queue.name],
            ["AWS/SQS", "NumberOfMessagesSent", "QueueName", aws_sqs_queue.analysis_queue.name],
            ["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", aws_sqs_queue.analysis_dlq.name]
          ]
        }
      }
    ]
  })
} 