# Story Analysis Queue
resource "aws_sqs_queue" "story_analysis" {
  name                        = "${var.environment}-agile-stories-analysis.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
  deduplication_scope         = "messageGroup"
  fifo_throughput_limit       = "perMessageGroupId"
  visibility_timeout_seconds  = 900    # 15 minutes for long-running analysis
  message_retention_seconds   = 86400  # 1 day
  max_message_size            = 262144 # 256 KB
  delay_seconds               = 0

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.story_analysis_dlq.arn
    maxReceiveCount     = 3
  })

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# Story Analysis Dead Letter Queue
resource "aws_sqs_queue" "story_analysis_dlq" {
  name                        = "${var.environment}-agile-stories-analysis-dlq.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
  message_retention_seconds   = 1209600 # 14 days

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# Story Estimation Queue
resource "aws_sqs_queue" "story_estimation" {
  name                        = "${var.environment}-agile-stories-estimation.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
  deduplication_scope         = "messageGroup"
  fifo_throughput_limit       = "perMessageGroupId"
  visibility_timeout_seconds  = 900    # 15 minutes for parallel estimations
  message_retention_seconds   = 86400  # 1 day
  max_message_size            = 262144 # 256 KB
  delay_seconds               = 0

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.story_estimation_dlq.arn
    maxReceiveCount     = 3
  })

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# Story Estimation Dead Letter Queue
resource "aws_sqs_queue" "story_estimation_dlq" {
  name                        = "${var.environment}-agile-stories-estimation-dlq.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
  message_retention_seconds   = 1209600 # 14 days

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# IAM Policy for Lambda access to SQS
resource "aws_iam_policy" "sqs_access" {
  name = "${var.environment}-agile-stories-sqs-access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
          "sqs:ChangeMessageVisibility"
        ]
        Resource = [
          aws_sqs_queue.story_analysis.arn,
          aws_sqs_queue.story_analysis_dlq.arn,
          aws_sqs_queue.story_estimation.arn,
          aws_sqs_queue.story_estimation_dlq.arn
        ]
      }
    ]
  })
} 