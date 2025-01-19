# Core infrastructure components

# Reference existing VPC
data "aws_vpc" "existing" {
  cidr_block = "10.0.0.0/16"
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.existing.id]
  }

  tags = {
    Type = "Private"
  }
}

# API Gateway
module "api_gateway" {
  source = "./modules/api_gateway"

  environment = var.environment
  vpc_id      = var.vpc_id
  subnet_ids  = var.subnet_ids

  cors_allowed_origins = var.cors_allowed_origins

  analyze_story_lambda_arn  = module.lambda_functions.analyze_story_lambda_arn
  estimate_story_lambda_arn = module.lambda_functions.estimate_story_lambda_arn
  get_status_lambda_arn     = module.lambda_functions.get_status_lambda_arn

  analyze_story_lambda_name  = module.lambda_functions.analyze_story_lambda_name
  estimate_story_lambda_name = module.lambda_functions.estimate_story_lambda_name
  get_status_lambda_name     = module.lambda_functions.get_status_lambda_name
}

# DynamoDB Tables
module "dynamodb" {
  source      = "./modules/dynamodb"
  environment = var.environment
}

# SQS Queues
module "queues" {
  source = "./modules/sqs"

  environment = var.environment
  prefix      = "${var.environment}-agile-stories"

  alarm_actions = var.alarm_actions
  ok_actions    = var.ok_actions

  # Pass Lambda function names for metrics
  lambda_function_names = [
    module.lambda_functions.analyze_story_lambda_name,
    module.lambda_functions.estimate_story_lambda_name,
    module.lambda_functions.get_status_lambda_name
  ]
}

module "lambda" {
  source = "./modules/lambda"

  account_id     = var.account_id
  environment    = var.environment
  aws_region     = var.aws_region
  vpc_id         = var.vpc_id
  subnet_ids     = var.subnet_ids
  openai_api_key = var.openai_api_key

  # Lambda configurations for all functions
  analyze_story_package_path    = var.analyze_story_package_path
  technical_review_package_path = var.technical_review_package_path
  estimate_story_package_path   = var.estimate_story_package_path
  get_status_package_path       = var.get_status_package_path
}

module "frontend_hosting" {
  source = "./modules/frontend_hosting"

  # ... existing variables ...
  certificate_arn = "arn:aws:acm:us-east-1:784902437693:certificate/bb3dc266-1a3c-4a10-83c6-73e919be3844"
} 