# 1. AWS Configuration Variables
variable "account_id" {
  description = "AWS Account ID"
  type        = string
}

variable "environment" {
  description = "Environment name (e.g., dev, prod)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

# 2. VPC Configuration
variable "vpc_id" {
  description = "VPC ID where resources will be created"
  type        = string
}

variable "cidr_block" {
  description = "CIDR block for VPC"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

# 3. Subnet Configuration
variable "public_subnet_cidrs" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "private_subnet_cidrs" {
  description = "List of private subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.103.0/24", "10.0.104.0/24"]
}

# 4. Lambda Package Paths
variable "analyze_story_package_path" {
  description = "Path to analyze story Lambda package"
  type        = string
}

variable "analyze_story_worker_package_path" {
  description = "Path to analyze story worker Lambda package"
  type        = string
}

variable "team_estimate_package_path" {
  description = "Path to team estimate Lambda package"
  type        = string
}

variable "team_estimate_worker_package_path" {
  description = "Path to team estimate worker Lambda package"
  type        = string
}

variable "technical_review_package_path" {
  description = "Path to technical review Lambda package"
  type        = string
}

variable "technical_review_worker_package_path" {
  description = "Path to technical review worker Lambda package"
  type        = string
}

variable "get_status_package_path" {
  description = "Path to get status Lambda package"
  type        = string
}

variable "story_state_handler_package_path" {
  description = "Path to the story state handler Lambda package"
  type        = string
}

variable "workflow_signal_handler_package_path" {
  description = "Path to the workflow signal handler Lambda package"
  type        = string
}

# 5. API Configuration
variable "openai_api_key" {
  description = "OpenAI API Key (stored in AWS Secrets Manager)"
  type        = string
  default     = ""
}

variable "error_handler_package_path" {
  description = "Path to the error handler Lambda package"
  type        = string
  default     = "../../../backend/src/error_handler/package.zip"
}

variable "route53_zone_id" {
  description = "Route53 zone ID for the domain"
  type        = string
}

variable "domain_name" {
  description = "Primary domain name"
  type        = string
}

variable "domain_aliases" {
  description = "List of domain aliases for CloudFront"
  type        = list(string)
}

# Network Configuration
variable "public_subnet_ids" {
  description = "List of public subnet IDs"
  type        = list(string)
}

variable "subnet_ids" {
  description = "List of subnet IDs for Lambda functions"
  type        = list(string)
}

# DynamoDB Configuration
variable "dynamodb_table_name" {
  description = "Name of the main DynamoDB table"
  type        = string
}

variable "estimations_table_name" {
  description = "Name of the estimations DynamoDB table"
  type        = string
}

variable "estimations_table_arn" {
  description = "ARN of the estimations DynamoDB table"
  type        = string
}

variable "estimations_table_stream_arn" {
  description = "Stream ARN of the estimations DynamoDB table"
  type        = string
}

variable "tenant_index_name" {
  description = "Name of the tenant GSI index"
  type        = string
}

# API Configuration
variable "cors_allowed_origins" {
  description = "List of allowed CORS origins"
  type        = list(string)
}

variable "error_sns_topic_arn" {
  description = "ARN of the SNS topic for error notifications"
  type        = string
}