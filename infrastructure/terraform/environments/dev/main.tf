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
  cidr_block = var.vpc_cidr_block
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

# Agile Stories Module
module "agile_stories" {
  source = "../../modules/agile_stories"

  # VPC configuration
  cidr_block          = "10.0.0.0/16"
  public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnet_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]
  public_subnet_ids   = ["subnet-05c29484564e0db92"]
  

  # Required variables
  account_id                 = var.account_id
  environment                = var.environment
  aws_region                 = var.aws_region
  openai_api_key             = var.openai_api_key
  vpc_id                     = var.vpc_id
  subnet_ids                 = var.subnet_ids
  analyze_story_package_path = var.analyze_story_package_path
  estimate_story_package_path = var.estimate_story_package_path
  get_status_package_path    = var.get_status_package_path
}

# Lambda Functions Module
module "lambda_functions" {
  source = "../../modules/lambda"

  # Required inputs from other modules
  dynamodb_table_arn         = module.dynamodb.stories_table_arn
  terraform_locks_table_arn  = module.dynamodb.locks_table_arn
  stories_table_arn          = module.dynamodb.stories_table_arn
  estimations_table_arn      = module.dynamodb.estimations_table_arn

  # Other required variables
  account_id                 = var.account_id
  environment                = var.environment
  vpc_id                     = var.vpc_id
  subnet_ids                 = var.subnet_ids
  openai_api_key             = var.openai_api_key
  analyze_story_package_path = var.analyze_story_package_path
  estimate_story_package_path = var.estimate_story_package_path
  get_status_package_path    = var.get_status_package_path

  function_name = "${var.environment}-lambda-functions"
}

# DynamoDB Module
module "dynamodb" {
  source      = "../../modules/dynamodb"
  environment = var.environment
}
