# Dead Letter Queue for failed messages (create this FIRST)
resource "aws_sqs_queue" "analysis_dlq" {
  name                        = "${var.prefix}-analysis-dlq.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
  message_retention_seconds   = var.dlq_message_retention_seconds

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# Story Analysis Queue (create this SECOND, after DLQ)
resource "aws_sqs_queue" "analysis_queue" {
  name                        = "${var.prefix}-analysis.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
  visibility_timeout_seconds  = var.visibility_timeout_seconds
  message_retention_seconds   = var.message_retention_seconds

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.analysis_dlq.arn
    maxReceiveCount     = var.max_receive_count
  })

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }

  depends_on = [aws_sqs_queue.analysis_dlq] # Explicit dependency
}

# Story Estimation Queue
resource "aws_sqs_queue" "story_estimation" {
  name                        = "${var.environment}-agile-stories-estimation.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
  deduplication_scope         = "messageGroup"
  fifo_throughput_limit       = "perMessageGroupId"
  visibility_timeout_seconds  = var.visibility_timeout_seconds
  message_retention_seconds   = var.message_retention_seconds
  max_message_size            = 262144 # 256 KB
  delay_seconds               = 0

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.story_estimation_dlq.arn
    maxReceiveCount     = var.max_receive_count
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
  message_retention_seconds   = var.dlq_message_retention_seconds

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
          aws_sqs_queue.analysis_queue.arn,
          aws_sqs_queue.analysis_dlq.arn,
          aws_sqs_queue.story_estimation.arn,
          aws_sqs_queue.story_estimation_dlq.arn
        ]
      }
    ]
  })
} 