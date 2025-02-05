# Configure AWS Provider
provider "aws" {
  region = var.aws_region
}

locals {
  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# DynamoDB Tables
module "dynamodb" {
  source = "../dynamodb"

  environment                   = var.environment
  enable_point_in_time_recovery = true
  enable_server_side_encryption = true
  enable_stream                 = true
}

# SQS Queues
module "sqs" {
  source = "../sqs"

  prefix      = var.prefix
  environment = var.environment

  message_retention_seconds     = 86400
  visibility_timeout_seconds    = 900
  max_receive_count             = 3
  dlq_message_retention_seconds = 1209600

  alarm_actions              = var.alarm_actions
  ok_actions                 = var.ok_actions
  max_message_age_threshold  = 3600
  dlq_messages_threshold     = 1
  high_throughput_threshold  = 1000
  aws_region                 = var.aws_region
  dashboard_refresh_interval = 300

  cost_monitoring_thresholds = {
    lambda_monthly_threshold     = 10
    sqs_monthly_threshold        = 5
    dynamodb_monthly_threshold   = 5
    apigateway_monthly_threshold = 5
  }
  billing_currency = "USD"

  lambda_function_names = module.lambda.lambda_function_names
}

# Lambda Functions
module "lambda" {
  source = "../lambda"

  environment         = var.environment
  vpc_id              = var.vpc_id
  subnet_ids          = var.subnet_ids
  openai_api_key      = var.openai_api_key
  dynamodb_table_name = var.dynamodb_table_name
  error_sns_topic_arn = var.error_sns_topic_arn

  account_id = var.account_id
  aws_region = var.aws_region

  dynamodb_table_arn        = module.dynamodb.stories_table_arn
  stories_table_arn         = module.dynamodb.stories_table_arn
  stories_table_name        = module.dynamodb.stories_table_name
  stories_table_stream_arn  = module.dynamodb.stories_table_stream_arn
  terraform_locks_table_arn = module.dynamodb.terraform_locks_table_arn

  analyze_story_package_path           = var.analyze_story_package_path
  analyze_story_worker_package_path    = var.analyze_story_worker_package_path
  team_estimate_package_path           = var.team_estimate_package_path
  team_estimate_worker_package_path    = var.team_estimate_worker_package_path
  technical_review_package_path        = var.technical_review_package_path
  technical_review_worker_package_path = var.technical_review_worker_package_path
  get_status_package_path              = var.get_status_package_path
  story_state_handler_package_path    = var.story_state_handler_package_path

  log_retention_days     = 30
  lambda_memory_size     = 256
  lambda_timeout         = 30
  additional_policy_arns = []
  function_name          = "${var.environment}-agile-stories"

  analysis_queue_url = module.sqs.analysis_queue_url

  # Consolidated estimations table config and new variables
  estimations_table_name       = module.dynamodb.estimations_table_name
  estimations_table_arn        = module.dynamodb.estimations_table_arn
  estimations_table_stream_arn = module.dynamodb.estimations_table_stream_arn
  tenant_index_name            = module.dynamodb.tenant_index_name
  estimations_role_index_name  = module.dynamodb.estimations_role_index_name

  error_handler_package_path = var.error_handler_package_path
  workflow_signal_handler_package_path = var.workflow_signal_handler_package_path

  environment_variables = {
    STORIES_TABLE = module.dynamodb.stories_table_name
    ESTIMATES_TABLE = module.dynamodb.estimations_table_name
    OPENAI_API_KEY = var.openai_api_key
    TECHNICAL_REVIEW_LAMBDA_NAME = "${var.environment}-agile-stories-review"
  }

  attach_policy_statements = true
  policy_statements = {
    dynamodb = {
      effect = "Allow"
      actions = [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:Query"
      ]
      resources = [module.dynamodb.stories_table_arn]
    },
    lambda = {
      effect = "Allow"
      actions = [
        "lambda:InvokeFunction"
      ]
      resources = ["arn:aws:lambda:${var.aws_region}:${var.account_id}:function:${var.environment}-agile-stories-review"]
    }
  }

  tags = local.tags
}

# API Gateway
module "api_gateway" {
  source = "../api_gateway"

  environment          = var.environment
  vpc_id               = var.vpc_id
  subnet_ids           = var.subnet_ids
  cors_allowed_origins = var.cors_allowed_origins
  log_retention_days   = 30
  domain_aliases       = var.domain_aliases

  analyze_story_lambda_arn  = module.lambda.analyze_story_lambda_arn
  analyze_story_lambda_name = module.lambda.analyze_story_lambda_name

  team_estimate_lambda_arn  = module.lambda.team_estimate_lambda_arn
  team_estimate_lambda_name = module.lambda.team_estimate_lambda_name

  get_status_lambda_arn  = module.lambda.get_status_lambda_arn
  get_status_lambda_name = module.lambda.get_status_lambda_name

  analyze_story_worker_name = module.lambda.analyze_story_worker_name
  analyze_story_worker_arn  = module.lambda.analyze_story_worker_arn

  technical_review_lambda_arn  = module.lambda.technical_review_lambda_arn
  technical_review_lambda_name = module.lambda.technical_review_lambda_name
  
}

module "acm" {
  source = "../acm"
  providers = {
    aws.us-east-1 = aws.us-east-1
  }

  route53_zone_id = var.route53_zone_id
  domain_name     = var.domain_name
}

# Add Cognito module
module "cognito" {
  source = "../cognito"
  
  environment = var.environment
}
