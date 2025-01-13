# Core infrastructure components
module "vpc" {
  source = "../vpc"

  cidr_block           = var.cidr_block
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  public_subnet_ids    = var.public_subnet_ids
  environment          = var.environment
}

module "dynamodb" {
  source = "../dynamodb"

  environment = var.environment
}

module "lambda" {
  source = "../lambda"

  account_id                  = var.account_id
  environment                 = var.environment
  vpc_id                      = var.vpc_id     # Pass vpc_id
  subnet_ids                  = var.subnet_ids # Pass subnet_ids
  openai_api_key              = var.openai_api_key
  analyze_story_package_path  = var.analyze_story_package_path
  estimate_story_package_path = var.estimate_story_package_path
  get_status_package_path     = var.get_status_package_path
  stories_table_arn           = module.dynamodb.stories_table_arn
  estimations_table_arn       = module.dynamodb.estimations_table_arn
  terraform_locks_table_arn   = module.dynamodb.locks_table_arn
  dynamodb_table_arn          = module.dynamodb.stories_table_arn

  function_name = "${var.environment}-agile-stories"
}

module "sqs" {
  source = "../sqs"

  environment   = var.environment
  prefix        = "${var.environment}-agile-stories"
  alarm_actions = var.alarm_actions
  ok_actions    = var.ok_actions
  lambda_function_names = [
    module.lambda.analyze_story_lambda_name,
    module.lambda.estimate_story_lambda_name,
    module.lambda.get_status_lambda_name
  ]
}

module "api_gateway" {
  source = "../api_gateway"

  environment          = var.environment
  vpc_id               = var.vpc_id     # Pass vpc_id
  subnet_ids           = var.subnet_ids # Pass subnet_ids
  cors_allowed_origins = var.cors_allowed_origins

  analyze_story_lambda_arn  = module.lambda.analyze_story_lambda_arn
  estimate_story_lambda_arn = module.lambda.estimate_story_lambda_arn
  get_status_lambda_arn     = module.lambda.get_status_lambda_arn

  analyze_story_lambda_name  = module.lambda.analyze_story_lambda_name
  estimate_story_lambda_name = module.lambda.estimate_story_lambda_name
  get_status_lambda_name     = module.lambda.get_status_lambda_name
}