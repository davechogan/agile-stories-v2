# Combined CloudWatch Dashboard
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

      # Lambda Function Metrics
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
            # Invocations
            ["AWS/Lambda", "Invocations", "FunctionName", "${var.environment}-agile-stories-analyze-story"],
            [".", ".", ".", "${var.environment}-agile-stories-estimate-story"],
            [".", ".", ".", "${var.environment}-agile-stories-get-status"]
          ]
          period = 300
          region = var.aws_region
          title  = "Lambda Invocations"
        }
      },

      # Cost Overview
      {
        type   = "metric"
        x      = 0
        y      = 12
        width  = 24
        height = 6
        properties = {
          view    = "timeSeries"
          stacked = true
          metrics = [
            # Lambda Costs
            ["AWS/Billing", "EstimatedCharges", "ServiceName", "Lambda", "Currency", "USD"],
            # SQS Costs
            [".", ".", ".", "AWSQueueService", ".", "."],
            # DynamoDB Costs
            [".", ".", ".", "AmazonDynamoDB", ".", "."],
            # API Gateway Costs
            [".", ".", ".", "AmazonApiGateway", ".", "."],
            # CloudWatch Costs
            [".", ".", ".", "AmazonCloudWatch", ".", "."]
          ]
          period = 3600
          region = "us-east-1"
          title  = "Estimated Service Costs (USD)"
        }
      },

      # Alarm Status
      {
        type   = "alarm"
        x      = 0
        y      = 18
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