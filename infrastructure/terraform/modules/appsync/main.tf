# AppSync API
resource "aws_appsync_graphql_api" "story_api" {
  name                = "${var.environment}-story-api"
  authentication_type = "API_KEY"
  schema             = file("${path.module}/schema.graphql")
}

# IAM Role for AppSync to access DynamoDB
resource "aws_iam_role" "appsync_dynamodb" {
  name = "${var.environment}-appsync-dynamodb-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "appsync.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy for AppSync role
resource "aws_iam_role_policy" "appsync_dynamodb" {
  name = "${var.environment}-appsync-dynamodb-policy"
  role = aws_iam_role.appsync_dynamodb.id

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
          "arn:aws:dynamodb:*:*:table/${var.story_table_name}",
          "arn:aws:dynamodb:*:*:table/${var.story_table_name}/*"
        ]
      }
    ]
  })
}

# API Key for client authentication
resource "aws_appsync_api_key" "story_api_key" {
  api_id  = aws_appsync_graphql_api.story_api.id
  expires = timeadd(timestamp(), "8760h")
}

# DynamoDB as data source
resource "aws_appsync_datasource" "dynamodb" {
  api_id           = aws_appsync_graphql_api.story_api.id
  name             = "story_status_table"
  service_role_arn = aws_iam_role.appsync_dynamodb.arn
  type             = "AMAZON_DYNAMODB"

  dynamodb_config {
    table_name = var.story_table_name
  }
}

# Query Resolver
resource "aws_appsync_resolver" "get_story_status" {
  api_id      = aws_appsync_graphql_api.story_api.id
  type        = "Query"
  field       = "getStoryStatus"
  data_source = aws_appsync_datasource.dynamodb.name

  request_template = <<EOF
{
    "version": "2018-05-29",
    "operation": "GetItem",
    "key": {
        "story_id": $util.dynamodb.toDynamoDBJson($ctx.args.storyId)
    }
}
EOF

  response_template = "$util.toJson($ctx.result)"
} 