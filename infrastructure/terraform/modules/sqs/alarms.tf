# CloudWatch Alarms for Analysis Queue
resource "aws_cloudwatch_metric_alarm" "analysis_queue_age" {
  alarm_name          = "${var.environment}-analysis-queue-message-age"
  alarm_description   = "Alarm when messages are too old in the analysis queue"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "ApproximateAgeOfOldestMessage"
  namespace           = "AWS/SQS"
  period              = "300" # 5 minutes
  statistic           = "Maximum"
  threshold           = var.max_message_age_threshold
  treat_missing_data  = "notBreaching"

  dimensions = {
    QueueName = aws_sqs_queue.analysis_queue.name
  }

  alarm_actions = var.alarm_actions
  ok_actions    = var.ok_actions

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

resource "aws_cloudwatch_metric_alarm" "analysis_dlq_messages" {
  alarm_name          = "${var.environment}-analysis-dlq-messages"
  alarm_description   = "Alarm when there are messages in the analysis DLQ"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "ApproximateNumberOfMessagesVisible"
  namespace           = "AWS/SQS"
  period              = "300" # 5 minutes
  statistic           = "Maximum"
  threshold           = var.dlq_messages_threshold
  treat_missing_data  = "notBreaching"

  dimensions = {
    QueueName = aws_sqs_queue.analysis_dlq.name
  }

  alarm_actions = var.alarm_actions
  ok_actions    = var.ok_actions

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# CloudWatch Alarms for Estimation Queue
resource "aws_cloudwatch_metric_alarm" "estimation_queue_age" {
  alarm_name          = "${var.environment}-estimation-queue-message-age"
  alarm_description   = "Alarm when messages are too old in the estimation queue"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "ApproximateAgeOfOldestMessage"
  namespace           = "AWS/SQS"
  period              = "300" # 5 minutes
  statistic           = "Maximum"
  threshold           = var.max_message_age_threshold
  treat_missing_data  = "notBreaching"

  dimensions = {
    QueueName = aws_sqs_queue.story_estimation.name
  }

  alarm_actions = var.alarm_actions
  ok_actions    = var.ok_actions

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

resource "aws_cloudwatch_metric_alarm" "estimation_dlq_messages" {
  alarm_name          = "${var.environment}-estimation-dlq-messages"
  alarm_description   = "Alarm when there are messages in the estimation DLQ"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "ApproximateNumberOfMessagesVisible"
  namespace           = "AWS/SQS"
  period              = "300" # 5 minutes
  statistic           = "Maximum"
  threshold           = var.dlq_messages_threshold
  treat_missing_data  = "notBreaching"

  dimensions = {
    QueueName = aws_sqs_queue.story_estimation_dlq.name
  }

  alarm_actions = var.alarm_actions
  ok_actions    = var.ok_actions

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# High Throughput Alarm
resource "aws_cloudwatch_metric_alarm" "high_throughput" {
  alarm_name          = "${var.environment}-queue-high-throughput"
  alarm_description   = "Alarm when message throughput is unusually high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "NumberOfMessagesReceived"
  namespace           = "AWS/SQS"
  period              = "300" # 5 minutes
  statistic           = "Sum"
  threshold           = var.high_throughput_threshold
  treat_missing_data  = "notBreaching"

  dimensions = {
    QueueName = aws_sqs_queue.analysis_queue.name
  }

  alarm_actions = var.alarm_actions
  ok_actions    = var.ok_actions

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
} 