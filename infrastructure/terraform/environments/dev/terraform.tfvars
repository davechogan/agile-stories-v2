# Development environment configuration
environment = "dev"
aws_region  = "us-east-1"
account_id  = "784902437693"

# VPC Configuration
vpc_id     = "vpc-075ca467a1d924c87"
cidr_block = "10.0.0.0/16"

# Subnet Configuration
public_subnet_cidrs  = ["10.0.101.0/24", "10.0.102.0/24"]
private_subnet_cidrs = ["10.0.103.0/24", "10.0.104.0/24"]

# Availability Zones
availability_zones = ["us-east-1a", "us-east-1b"]

# Lambda package paths
analyze_story_package_path           = "../../../../backend/src/analyze_story/package.zip"
analyze_story_worker_package_path    = "../../../../backend/src/analyze_story_worker/package.zip"
team_estimate_package_path           = "../../../../backend/src/team_estimate/package.zip"
team_estimate_worker_package_path    = "../../../../backend/src/team_estimate_worker/package.zip"
technical_review_package_path        = "../../../../backend/src/technical_review/package.zip"
technical_review_worker_package_path = "../../../../backend/src/technical_review_worker/package.zip"
get_status_package_path              = "../../../../backend/src/get_status/package.zip"

# API Configuration
openai_api_key = "" # Note: comes from GitHub Secrets 