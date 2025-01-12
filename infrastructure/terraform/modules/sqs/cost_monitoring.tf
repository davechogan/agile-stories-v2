# Update the dashboard with cost monitoring widgets
resource "aws_cloudwatch_dashboard" "agile_stories" {
  # ... existing dashboard configuration ...

  dashboard_body = jsonencode({
    widgets = [
      # ... existing widgets ...
      
      # Cost Overview
      {
        type   = "metric"
        x      = 0
        y      = 30
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
          period = 3600  # 1 hour
          region = "us-east-1"  # Billing metrics are in us-east-1
          title  = "Estimated Service Costs (USD)"
        }
      },
      
      # Lambda Cost Details
      {
        type   = "metric"
        x      = 0
        y      = 36
        width  = 12
        height = 6
        properties = {
          view    = "timeSeries"
          stacked = false
          metrics = [
            # Lambda Duration Costs
            ["AWS/Lambda", "Duration", "FunctionName", "${var.environment}-agile-stories-analyze-story", 
             { id: "m1", stat: "Sum", unit: "Milliseconds", label: "Analysis Duration" }],
            [".", ".", ".", "${var.environment}-agile-stories-estimate-story",
             { id: "m2", stat: "Sum", unit: "Milliseconds", label: "Estimation Duration" }],
            [".", ".", ".", "${var.environment}-agile-stories-get-status",
             { id: "m3", stat: "Sum", unit: "Milliseconds", label: "Status Duration" }]
          ]
          period = 3600
          region = var.aws_region
          title  = "Lambda Duration Costs"
          annotations = {
            horizontal: [
              {
                value: 400000,  # Monthly free tier threshold
                label: "Free Tier Threshold"
              }
            ]
          }
        }
      },
      
      # SQS Usage Metrics
      {
        type   = "metric"
        x      = 12
        y      = 36
        width  = 12
        height = 6
        properties = {
          view    = "timeSeries"
          stacked = true
          metrics = [
            # Request Counts
            ["AWS/SQS", "NumberOfMessagesReceived", "QueueName", aws_sqs_queue.story_analysis.name],
            [".", "NumberOfMessagesSent", ".", "."],
            [".", "NumberOfMessagesReceived", ".", aws_sqs_queue.story_estimation.name],
            [".", "NumberOfMessagesSent", ".", "."]
          ]
          period = 3600
          region = var.aws_region
          title  = "SQS Request Costs"
          annotations = {
            horizontal: [
              {
                value: 1000000,  # Monthly free tier threshold
                label: "Free Tier Threshold"
              }
            ]
          }
        }
      },
      
      # DynamoDB Capacity
      {
        type   = "metric"
        x      = 0
        y      = 42
        width  = 12
        height = 6
        properties = {
          view    = "timeSeries"
          stacked = false
          metrics = [
            # Read/Write Units
            ["AWS/DynamoDB", "ConsumedReadCapacityUnits", "TableName", "${var.environment}-agile-stories"],
            [".", "ConsumedWriteCapacityUnits", ".", "."],
            [".", "ConsumedReadCapacityUnits", ".", "${var.environment}-agile-stories-estimations"],
            [".", "ConsumedWriteCapacityUnits", ".", "."]
          ]
          period = 3600
          region = var.aws_region
          title  = "DynamoDB Capacity Usage"
        }
      },
      
      # API Gateway Requests
      {
        type   = "metric"
        x      = 12
        y      = 42
        width  = 12
        height = 6
        properties = {
          view    = "timeSeries"
          stacked = false
          metrics = [
            ["AWS/ApiGateway", "Count", "ApiId", "${var.environment}-agile-stories-api"],
            [".", "4XXError", ".", "."],
            [".", "5XXError", ".", "."]
          ]
          period = 3600
          region = var.aws_region
          title  = "API Gateway Usage"
          annotations = {
            horizontal: [
              {
                value: 1000000,  # Monthly free tier threshold
                label: "Free Tier Threshold"
              }
            ]
          }
        }
      }
    ]
  })
} 