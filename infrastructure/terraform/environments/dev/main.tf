terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Fetch existing VPC
data "aws_vpc" "existing" {
  id = "vpc-075ca467a1d924c87"
}

# Fetch private subnets in the VPC
data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.existing.id]
  }

  tags = {
    Type = "Private"
  }
}

# Variables for VPC configuration
variable "vpc_cidr_block" {
  default = "10.0.0.0/16"
}

# Retrieve OpenAI API Key from Secrets Manager
data "aws_secretsmanager_secret" "openai_key" {
  name = "openai_key"
}

data "aws_secretsmanager_secret_version" "openai_key_version" {
  secret_id = data.aws_secretsmanager_secret.openai_key.id
}

# Agile Stories Module
module "agile_stories" {
  source = "../../modules/agile_stories"

  # Required variables
  account_id                           = var.account_id
  environment                          = var.environment
  aws_region                           = var.aws_region
  openai_api_key                       = data.aws_secretsmanager_secret_version.openai_key_version.secret_string
  vpc_id                               = var.vpc_id
  subnet_ids                           = var.subnet_ids
  public_subnet_ids                    = var.public_subnet_ids
  cidr_block                          = var.cidr_block
  public_subnet_cidrs                 = var.public_subnet_cidrs
  private_subnet_cidrs                = var.private_subnet_cidrs

  # Lambda package paths
  analyze_story_package_path           = var.analyze_story_package_path
  analyze_story_worker_package_path    = var.analyze_story_worker_package_path
  team_estimate_package_path           = var.team_estimate_package_path
  team_estimate_worker_package_path    = var.team_estimate_worker_package_path
  technical_review_package_path        = var.technical_review_package_path
  technical_review_worker_package_path = var.technical_review_worker_package_path
  get_status_package_path             = var.get_status_package_path
}

# Lambda Functions Module
module "lambda_functions" {
  source = "../../modules/lambda"

  # Required inputs from other modules
  dynamodb_table_arn        = module.dynamodb.stories_table_arn
  terraform_locks_table_arn = module.dynamodb.locks_table_arn
  stories_table_arn         = module.dynamodb.stories_table_arn
  estimations_table_arn     = module.dynamodb.estimations_table_arn

  # Other required variables
  account_id                  = var.account_id
  environment                 = var.environment
  vpc_id                      = var.vpc_id
  subnet_ids                  = var.subnet_ids
  openai_api_key              = data.aws_secretsmanager_secret_version.openai_key_version.secret_string
  analyze_story_package_path  = "../../../../backend/src/analyze_story/package.zip"
  analyze_story_worker_package_path    = "../../../../backend/src/analyze_story_worker/package.zip"
  team_estimate_package_path           = "../../../../backend/src/team_estimate/package.zip"
  team_estimate_worker_package_path    = "../../../../backend/src/team_estimate_worker/package.zip"
  technical_review_package_path        = "../../../../backend/src/technical_review/package.zip"
  technical_review_worker_package_path = "../../../../backend/src/technical_review_worker/package.zip"
  get_status_package_path             = "../../../../backend/src/get_status/package.zip"

  function_name = "${var.environment}-lambda-functions"
}

# DynamoDB Module
module "dynamodb" {
  source      = "../../modules/dynamodb"
  environment = var.environment
}
