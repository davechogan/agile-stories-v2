variable "environment" {
  description = "Environment name (dev/prod)"
  type        = string
}

variable "account_id" {
  description = "AWS account ID"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
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

# Lambda package paths
variable "analyze_story_package_path" {
  description = "Path to analyze story Lambda package"
  type        = string
}

variable "technical_review_package_path" {
  description = "Path to technical review Lambda package"
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