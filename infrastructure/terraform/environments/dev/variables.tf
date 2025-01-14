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

variable "vpc_id" {
  description = "VPC ID where resources will be created"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for the resources"
  type        = list(string)
}

variable "openai_api_key" {
  description = "OpenAI API Key (stored in AWS Secrets Manager)"
  type        = string
  default     = ""
}

# Lambda package paths
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

# Other variables from terraform.tfvars that need declaration
variable "dlq_messages_threshold" {
  description = "Threshold for DLQ messages alarm"
  type        = number
  default     = 1
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "lambda_memory_size" {
  description = "Memory size for Lambda functions in MB"
  type        = number
  default     = 256
}

variable "enable_detailed_monitoring" {
  description = "Enable detailed CloudWatch monitoring"
  type        = bool
  default     = false
}

# Add these variables
variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "lambda_timeout" {
  description = "Timeout for Lambda functions"
  type        = number
  default     = 30
}

variable "cidr_block" {
  description = "CIDR block for VPC"
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
  description = "List of public subnet IDs"
  type        = list(string)
} 