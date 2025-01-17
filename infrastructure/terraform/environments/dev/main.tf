# 1. Provider Configuration
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 2. Variables
variable "vpc_cidr_block" {
  default = "10.0.0.0/16"
}

# 3. Data Sources
data "aws_vpc" "existing" {
  id = "vpc-075ca467a1d924c87"
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

data "aws_secretsmanager_secret" "openai_key" {
  name = "openai_key"
}

data "aws_secretsmanager_secret_version" "openai_key_version" {
  secret_id = data.aws_secretsmanager_secret.openai_key.id
}

# 4. Infrastructure Layer
module "vpc" {
  source = "../../modules/vpc"

  environment = var.environment
  cidr_block  = var.vpc_cidr

  public_subnet_cidrs  = ["10.0.101.0/24", "10.0.102.0/24"]
  private_subnet_cidrs = ["10.0.103.0/24", "10.0.104.0/24"]

  public_subnet_ids  = []
  availability_zones = ["us-east-1a", "us-east-1b"]
}

# 5. Application Layer
module "agile_stories" {
  source = "../../modules/agile_stories"

  subnet_ids          = module.vpc.private_subnet_ids
  public_subnet_ids   = module.vpc.public_subnet_ids
  vpc_id              = module.vpc.vpc_id
  error_sns_topic_arn = aws_sns_topic.error_notifications.arn

  account_id           = var.account_id
  environment          = var.environment
  aws_region           = var.aws_region
  openai_api_key       = data.aws_secretsmanager_secret_version.openai_key_version.secret_string
  cidr_block           = var.cidr_block
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs

  analyze_story_package_path           = var.analyze_story_package_path
  analyze_story_worker_package_path    = var.analyze_story_worker_package_path
  team_estimate_package_path           = var.team_estimate_package_path
  team_estimate_worker_package_path    = var.team_estimate_worker_package_path
  technical_review_package_path        = var.technical_review_package_path
  technical_review_worker_package_path = var.technical_review_worker_package_path
  get_status_package_path              = var.get_status_package_path
  error_handler_package_path           = var.error_handler_package_path

  estimations_table_name       = "${var.environment}-agile-stories-estimations"
  estimations_table_arn        = "arn:aws:dynamodb:${var.aws_region}:${var.account_id}:table/${var.environment}-agile-stories-estimations"
  estimations_table_stream_arn = "arn:aws:dynamodb:${var.aws_region}:${var.account_id}:table/${var.environment}-agile-stories-estimations/stream/*"
  tenant_index_name            = "tenant-index"
  dynamodb_table_name          = "${var.environment}-agile-stories"
}

module "step_functions" {
  source      = "../../modules/step_functions"
  name_prefix = "dev"
  environment = var.environment
  lambda_arns = [
    module.agile_stories.analyze_story_lambda_arn,
    module.agile_stories.analyze_story_worker_lambda_arn,
    module.agile_stories.technical_review_lambda_arn,
    module.agile_stories.technical_review_worker_lambda_arn,
    module.agile_stories.team_estimate_lambda_arn,
    module.agile_stories.team_estimate_worker_lambda_arn
  ]
  workflow_definition = templatefile(
    "${path.module}/../../modules/step_functions/workflow.json",
    {
      analyze_story_arn           = module.agile_stories.analyze_story_lambda_arn,
      analyze_story_worker_arn    = module.agile_stories.analyze_story_worker_lambda_arn,
      technical_review_arn        = module.agile_stories.technical_review_lambda_arn,
      technical_review_worker_arn = module.agile_stories.technical_review_worker_lambda_arn,
      team_estimate_arn           = module.agile_stories.team_estimate_lambda_arn,
      team_estimate_worker_arn    = module.agile_stories.team_estimate_worker_lambda_arn
    }
  )
}

resource "aws_sns_topic" "error_notifications" {
  name = "error-notifications"
}

module "frontend_hosting" {
  source      = "../../modules/frontend_hosting"
  environment = var.environment
}

# Update to use CloudFront domain
output "frontend_url" {
  value = module.frontend_hosting.cloudfront_domain
}

output "cloudfront_id" {
  value = module.frontend_hosting.cloudfront_id
}

module "appsync" {
  source           = "../../modules/appsync"
  environment      = var.environment
  story_table_name = "${var.environment}-agile-stories"
}

output "appsync_endpoint" {
  value = module.appsync.api_endpoint
}

output "appsync_api_key" {
  value     = module.appsync.api_key
  sensitive = true
}


