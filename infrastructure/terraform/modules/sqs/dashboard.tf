resource "aws_cloudwatch_dashboard" "agile_stories" {
  dashboard_name = "${var.environment}-agile-stories-monitoring"

  dashboard_body = jsonencode({
    widgets = [
      # Queue Overview
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          view    = "timeSeries"
          stacked = false
          metrics = [
            # Analysis Queue Metrics
            ["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", aws_sqs_queue.story_analysis.name],
            [".", "ApproximateAgeOfOldestMessage", ".", "."],
            [".", "NumberOfMessagesReceived", ".", "."],
            [".", "NumberOfMessagesSent", ".", "."],
            # Estimation Queue Metrics
            ["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", aws_sqs_queue.story_estimation.name],
            [".", "ApproximateAgeOfOldestMessage", ".", "."],
            [".", "NumberOfMessagesReceived", ".", "."],
            [".", "NumberOfMessagesSent", ".", "."]
          ]
          period = 300
          region = var.aws_region
          title  = "Queue Metrics Overview"
        }
      },
      # DLQ Status
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6
        properties = {
          view    = "timeSeries"
          stacked = false
          metrics = [
            ["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", aws_sqs_queue.story_analysis_dlq.name],
            [".", ".", ".", aws_sqs_queue.story_estimation_dlq.name]
          ]
          period = 300
          region = var.aws_region
          title  = "Dead Letter Queue Messages"
        }
      },
      # Queue Performance
      {
        type   = "metric"
        x      = 0
        y      = 6
        width  = 12
        height = 6
        properties = {
          view    = "timeSeries"
          stacked = false
          metrics = [
            # Analysis Queue Performance
            ["AWS/SQS", "SentMessageSize", "QueueName", aws_sqs_queue.story_analysis.name],
            [".", "NumberOfMessagesDeleted", ".", "."],
            [".", "NumberOfEmptyReceives", ".", "."],
            # Estimation Queue Performance
            ["AWS/SQS", "SentMessageSize", "QueueName", aws_sqs_queue.story_estimation.name],
            [".", "NumberOfMessagesDeleted", ".", "."],
            [".", "NumberOfEmptyReceives", ".", "."]
          ]
          period = 300
          region = var.aws_region
          title  = "Queue Performance Metrics"
        }
      },
      # Error Tracking
      {
        type   = "metric"
        x      = 12
        y      = 6
        width  = 12
        height = 6
        properties = {
          view    = "timeSeries"
          stacked = false
          metrics = [
            ["AWS/SQS", "NumberOfMessagesMoved", "QueueName", aws_sqs_queue.story_analysis.name],
            [".", ".", ".", aws_sqs_queue.story_estimation.name],
            [".", "ApproximateAgeOfOldestMessage", ".", aws_sqs_queue.story_analysis_dlq.name],
            [".", ".", ".", aws_sqs_queue.story_estimation_dlq.name]
          ]
          period = 300
          region = var.aws_region
          title  = "Error Tracking"
        }
      },
      # Alarm Status
      {
        type   = "alarm"
        x      = 0
        y      = 12
        width  = 24
        height = 6
        properties = {
          alarms = [
            aws_cloudwatch_metric_alarm.analysis_queue_age.arn,
            aws_cloudwatch_metric_alarm.analysis_dlq_messages.arn,
            aws_cloudwatch_metric_alarm.estimation_queue_age.arn,
            aws_cloudwatch_metric_alarm.estimation_dlq_messages.arn,
            aws_cloudwatch_metric_alarm.high_throughput.arn
          ]
          title = "Queue Alarms Status"
        }
      }
    ]
  })
} 