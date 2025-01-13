resource "aws_cloudwatch_metric_alarm" "analysis_queue_age" {
  alarm_name          = "${var.prefix}-analysis-queue-age"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name        = "ApproximateAgeOfOldestMessage"
  namespace          = "AWS/SQS"
  period            = "300"
  statistic         = "Maximum"
  threshold         = "3600"  # 1 hour
  alarm_description = "Analysis queue message age is too high"
  alarm_actions     = []

  dimensions = {
    QueueName = "${var.prefix}-analysis.fifo"
  }
}

resource "aws_cloudwatch_metric_alarm" "analysis_dlq_messages" {
  alarm_name          = "${var.prefix}-analysis-dlq-messages"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name        = "ApproximateNumberOfMessagesVisible"
  namespace          = "AWS/SQS"
  period            = "300"
  statistic         = "Maximum"
  threshold         = "0"
  alarm_description = "Messages detected in Analysis DLQ"
  alarm_actions     = []

  dimensions = {
    QueueName = "${var.prefix}-analysis-dlq.fifo"
  }
}

resource "aws_cloudwatch_metric_alarm" "high_throughput" {
  # ... other settings ...
  dimensions = {
    QueueName = aws_sqs_queue.analysis_queue.name
  }
} 