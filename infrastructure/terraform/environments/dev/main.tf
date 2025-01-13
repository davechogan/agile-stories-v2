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

module "agile_stories" {
  source = "../../" # Points to root module

  environment = "dev"
  aws_region  = "us-east-1"

  # VPC and subnet configuration
  vpc_id = "vpc-075ca467a1d924c87"
  subnet_ids = [
    "subnet-05c29484564e0db92",
    "subnet-027bcb766a648dab3"
  ]

  # Development specific configurations
  cors_allowed_origins = ["*"] # More permissive for development

  # Development packages
  analyze_story_package_path  = "../../../backend/dist/analyze_story.zip"
  estimate_story_package_path = "../../../backend/dist/estimate_story.zip"
  get_status_package_path     = "../../../backend/dist/get_status.zip"

  # Dev environment variables
  openai_api_key = var.openai_api_key
} 