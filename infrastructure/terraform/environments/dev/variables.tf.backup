variable "account_id" {
  description = "AWS account ID"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs"
  type        = list(string)
}

variable "openai_api_key" {
  description = "OpenAI API Key"
  type        = string
  sensitive   = true
}

variable "analyze_story_package_path" {
  description = "Path to analyze story Lambda package"
  type        = string
}

variable "estimate_story_package_path" {
  description = "Path to estimate story Lambda package"
  type        = string
}

variable "get_status_package_path" {
  description = "Path to get status Lambda package"
  type        = string
} 