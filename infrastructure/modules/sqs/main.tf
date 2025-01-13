resource "aws_sqs_queue" "analysis_queue" {
  name                        = "${var.prefix}-analysis.fifo"
  fifo_queue                 = true
  content_based_deduplication = true
  visibility_timeout_seconds  = 900  # 15 minutes
  message_retention_seconds   = 1209600  # 14 days
  
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.analysis_dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_sqs_queue" "analysis_dlq" {
  name                        = "${var.prefix}-analysis-dlq.fifo"
  fifo_queue                 = true
  content_based_deduplication = true
  message_retention_seconds   = 1209600  # 14 days
}

resource "aws_iam_policy" "sqs_access" {
  name        = "${var.prefix}-sqs-access"
  description = "Policy for SQS access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = [
          aws_sqs_queue.analysis_queue.arn,
          aws_sqs_queue.analysis_dlq.arn
        ]
      }
    ]
  })
} 