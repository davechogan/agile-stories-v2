# Stories table
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

  attribute {
    name = "tenant_id"
    type = "S"
  }

  attribute {
    name = "token"
    type = "S"
  }

  global_secondary_index {
    name            = "tenant-index"
    hash_key        = "tenant_id"
    range_key       = "story_id"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "token-index"
    hash_key        = "token"
    projection_type = "ALL"
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
  }
}

# Estimations table
resource "aws_dynamodb_table" "estimations" {
  name         = "${var.environment}-agile-stories-estimations"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "estimation_id"
  range_key    = "story_id"

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

  attribute {
    name = "tenantId"
    type = "S"
  }

  global_secondary_index {
    name            = "story-created-index"
    hash_key        = "story_id"
    range_key       = "created_at"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "tenant-index"
    hash_key        = "tenantId"
    range_key       = "story_id"
    projection_type = "ALL"
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

