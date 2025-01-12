# Lambda CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  for_each = toset([
    "analyze-story",
    "estimate-story",
    "get-status"
  ])

  alarm_name          = "${var.environment}-${each.key}-errors"
  alarm_description   = "Alarm when Lambda function has errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name        = "Errors"
  namespace          = "AWS/Lambda"
  period             = "300"  # 5 minutes
  statistic          = "Sum"
  threshold          = "0"
  treat_missing_data = "notBreaching"

  dimensions = {
    FunctionName = "${var.environment}-agile-stories-${each.key}"
  }

  alarm_actions = var.alarm_actions
  ok_actions    = var.ok_actions

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# Update the dashboard with Lambda metrics
resource "aws_cloudwatch_dashboard" "agile_stories" {
  # ... existing dashboard configuration ...

  dashboard_body = jsonencode({
    widgets = [
      # ... existing widgets ...
      
      # Lambda Function Metrics
      {
        type   = "metric"
        x      = 0
        y      = 18
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
      {
        type   = "metric"
        x      = 12
        y      = 18
        width  = 12
        height = 6
        properties = {
          view    = "timeSeries"
          stacked = false
          metrics = [
            # Errors
            ["AWS/Lambda", "Errors", "FunctionName", "${var.environment}-agile-stories-analyze-story"],
            [".", ".", ".", "${var.environment}-agile-stories-estimate-story"],
            [".", ".", ".", "${var.environment}-agile-stories-get-status"]
          ]
          period = 300
          region = var.aws_region
          title  = "Lambda Errors"
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 24
        width  = 12
        height = 6
        properties = {
          view    = "timeSeries"
          stacked = false
          metrics = [
            # Duration
            ["AWS/Lambda", "Duration", "FunctionName", "${var.environment}-agile-stories-analyze-story"],
            [".", ".", ".", "${var.environment}-agile-stories-estimate-story"],
            [".", ".", ".", "${var.environment}-agile-stories-get-status"]
          ]
          period = 300
          region = var.aws_region
          title  = "Lambda Duration"
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 24
        width  = 12
        height = 6
        properties = {
          view    = "timeSeries"
          stacked = false
          metrics = [
            # Throttles
            ["AWS/Lambda", "Throttles", "FunctionName", "${var.environment}-agile-stories-analyze-story"],
            [".", ".", ".", "${var.environment}-agile-stories-estimate-story"],
            [".", ".", ".", "${var.environment}-agile-stories-get-status"],
            # Concurrent Executions
            [".", "ConcurrentExecutions", ".", "${var.environment}-agile-stories-analyze-story"],
            [".", ".", ".", "${var.environment}-agile-stories-estimate-story"],
            [".", ".", ".", "${var.environment}-agile-stories-get-status"]
          ]
          period = 300
          region = var.aws_region
          title  = "Lambda Throttling and Concurrency"
        }
      }
    ]
  })
} 