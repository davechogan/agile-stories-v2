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

  subnet_ids        = module.vpc.private_subnet_ids
  public_subnet_ids = module.vpc.public_subnet_ids
  vpc_id           = module.vpc.vpc_id

  account_id       = var.account_id
  environment      = var.environment
  aws_region       = var.aws_region
  openai_api_key   = data.aws_secretsmanager_secret_version.openai_key_version.secret_string
  cidr_block       = var.cidr_block
  public_subnet_cidrs = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs

  analyze_story_package_path           = var.analyze_story_package_path
  analyze_story_worker_package_path    = var.analyze_story_worker_package_path
  team_estimate_package_path           = var.team_estimate_package_path
  team_estimate_worker_package_path    = var.team_estimate_worker_package_path
  technical_review_package_path        = var.technical_review_package_path
  technical_review_worker_package_path = var.technical_review_worker_package_path
  get_status_package_path             = var.get_status_package_path
}
