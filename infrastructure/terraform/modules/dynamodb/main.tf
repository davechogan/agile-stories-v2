# Stories Table
resource "aws_dynamodb_table" "agile_stories" {
  name         = "${var.environment}-agile-stories"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "story_id"
  range_key    = "version"

  attribute {
    name = "story_id"
    type = "S"
  }

  attribute {
    name = "version"
    type = "S"
  }

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# Estimations Table
resource "aws_dynamodb_table" "estimations" {
  name             = "${var.environment}-agile-stories-estimations"
  billing_mode     = "PAY_PER_REQUEST"
  hash_key         = "estimation_id"
  range_key        = "story_id"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "estimation_id"
    type = "S"
  }

  attribute {
    name = "story_id"
    type = "S"
  }

  attribute {
    name = "created_at"
    type = "S"
  }


  # GSI for story queries
  global_secondary_index {
    name            = "story-created-index"
    hash_key        = "story_id"
    range_key       = "created_at"
    projection_type = "ALL"
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled = true
  }

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# IAM Policy for Lambda access to DynamoDB
resource "aws_iam_policy" "dynamodb_access" {
  name = "${var.environment}-agile-stories-dynamodb-access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          aws_dynamodb_table.agile_stories.arn,
          "${aws_dynamodb_table.agile_stories.arn}/index/*",
          aws_dynamodb_table.estimations.arn,
          "${aws_dynamodb_table.estimations.arn}/index/*"
        ]
      }
    ]
  })
}

# Terraform state locking table
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "agile-stories-terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  point_in_time_recovery {
    enabled = var.enable_point_in_time_recovery
  }

  server_side_encryption {
    enabled = var.enable_server_side_encryption
  }

  stream_enabled   = var.enable_stream
  stream_view_type = var.enable_stream ? "NEW_AND_OLD_IMAGES" : null

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

