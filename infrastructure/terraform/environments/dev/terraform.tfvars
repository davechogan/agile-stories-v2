# Development environment configuration
environment = "dev"
aws_region  = "us-east-1"
account_id  = "784902437693"

# VPC Configuration
vpc_id     = "vpc-09557185ab87a01df"
cidr_block = "10.0.0.0/16"

# Subnet Configuration
public_subnet_cidrs  = ["10.0.101.0/24", "10.0.102.0/24"]
private_subnet_cidrs = ["10.0.103.0/24", "10.0.104.0/24"]

# Availability Zones
availability_zones = ["us-east-1a", "us-east-1b"]

# Domain configuration
route53_zone_id = "Z0322690VKZ8IYUCFYBU"
domain_name     = "agile-advisor.com"
domain_aliases  = [
  "www.agile-advisor.com",
  "agile-advisor.com",
  
]

# Lambda package paths
analyze_story_package_path           = "../../../../backend/src/analyze_story/package.zip"
analyze_story_worker_package_path    = "../../../../backend/src/analyze_story_worker/package.zip"
team_estimate_package_path           = "../../../../backend/src/team_estimate/package.zip"
team_estimate_worker_package_path    = "../../../../backend/src/team_estimate_worker/package.zip"
technical_review_package_path        = "../../../../backend/src/technical_review/package.zip"
technical_review_worker_package_path = "../../../../backend/src/technical_review_worker/package.zip"
get_status_package_path             = "../../../../backend/src/get_status/package.zip"
error_handler_package_path          = "../../../../backend/src/error_handler/package.zip"
story_state_handler_package_path    = "../../../../backend/src/story_state_handler/package.zip"
workflow_signal_handler_package_path = "../../../../backend/src/workflow_signal_handler/package.zip"

# API Configuration
openai_api_key = "" # Note: comes from GitHub Secrets

# Add the new required variables
cors_allowed_origins = [
  "https://agile-advisor.com",
  "https://www.agile-advisor.com",
  "https://dx767f9d1kgyp.cloudfront.net"
]

# Public subnet IDs (from public[0] and public[1])
public_subnet_ids = [
  "subnet-0cd54c29ff5ce03b5",  # dev-public-subnet-1 (us-east-1a)
  "subnet-0e1feb39dfc37113d"   # dev-public-subnet-2 (us-east-1b)
]

# Private subnet IDs (from private[0] and private[1])
subnet_ids = [
  "subnet-042afee183857b464",  # dev-private-subnet-1 (us-east-1a)
  "subnet-029ee2ae820d228f8"   # dev-private-subnet-2 (us-east-1b)
]

# DynamoDB Configuration
dynamodb_table_name = "dev-agile-stories"
estimations_table_name = "dev-agile-stories-estimations"
estimations_table_arn = "arn:aws:dynamodb:us-east-1:784902437693:table/dev-agile-stories-estimations"
estimations_table_stream_arn = "arn:aws:dynamodb:us-east-1:784902437693:table/dev-agile-stories-estimations/stream/timestamp"
tenant_index_name = "tenant-index"

# Error handling
error_sns_topic_arn = "arn:aws:sns:us-east-1:784902437693:dev-agile-stories-errors" 

cloudfront_distribution_id = "E2BP3G13C91WFS" 