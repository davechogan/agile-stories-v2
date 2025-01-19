variable "environment" {
  description = "Environment name (dev, prod, etc)"
  type        = string
}

variable "account_id" {
  description = "AWS account ID"
  type        = string
}

variable "openai_api_key" {
  description = "OpenAI API key for Lambda functions"
  type        = string
  sensitive   = true
}

variable "analyze_story_package_path" {
  description = "Path to the analyze story Lambda package"
  type        = string
}

variable "analyze_story_worker_package_path" {
  description = "Path to the analyze story worker Lambda package"
  type        = string
}

variable "team_estimate_package_path" {
  description = "Path to the team estimate Lambda package"
  type        = string
}

variable "team_estimate_worker_package_path" {
  description = "Path to the team estimate worker Lambda package"
  type        = string
}

variable "technical_review_package_path" {
  description = "Path to the technical review Lambda package"
  type        = string
}

variable "technical_review_worker_package_path" {
  description = "Path to the technical review worker Lambda package"
  type        = string
}

variable "get_status_package_path" {
  description = "Path to the get status Lambda package"
  type        = string
}
variable "alarm_actions" {
  description = "List of ARNs to notify when an alarm triggers"
  type        = list(string)
  default     = []
}

variable "ok_actions" {
  description = "List of ARNs to notify when an alarm returns to OK state"
  type        = list(string)
  default     = []
}

variable "cors_allowed_origins" {
  description = "Allowed origins for CORS on the API Gateway"
  type        = list(string)
  default     = ["*"]
}

variable "aws_region" {
  description = "AWS region where the resources will be deployed"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC where resources will be deployed"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for the resources"
  type        = list(string)
}

variable "cidr_block" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
}

variable "public_subnet_ids" {
  description = "List of public subnet IDs for the VPC"
  type        = list(string)
}

variable "prefix" {
  description = "Prefix for resource names"
  type        = string
  default     = "agile-stories"
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
  description = "Name of the tenant GSI for DynamoDB tables"
  type        = string
}

variable "error_sns_topic_arn" {
  description = "ARN of the error notification SNS topic"
  type        = string
}
variable "error_handler_package_path" {
  description = "Path to the error handler Lambda package"
  type        = string
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  type        = string
}

variable "route53_zone_id" {
  description = "Route53 zone ID for the domain"
  type        = string
}

variable "domain_aliases" {
  description = "List of domain aliases for the API Gateway"
  type        = list(string)
}

variable "domain_name" {
  description = "Domain name for ACM certificate"
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
