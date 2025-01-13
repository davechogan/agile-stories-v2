variable "account_id" {
  description = "AWS account ID"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "cors_allowed_origins" {
  description = "List of allowed origins for CORS"
  type        = list(string)
  default     = ["*"]
}

variable "openai_api_key" {
  description = "OpenAI API key for Lambda functions"
  type        = string
  sensitive   = true
}

variable "analyze_story_package_path" {
  description = "Path to the analyze story Lambda deployment package"
  type        = string
}

variable "estimate_story_package_path" {
  description = "Path to the estimate story Lambda deployment package"
  type        = string
}

variable "get_status_package_path" {
  description = "Path to the get status Lambda deployment package"
  type        = string
}

variable "alarm_actions" {
  description = "List of ARNs to notify when alarm triggers"
  type        = list(string)
  default     = []
}

variable "ok_actions" {
  description = "List of ARNs to notify when alarm returns to OK state"
  type        = list(string)
  default     = []
}

variable "vpc_id" {
  description = "ID of the VPC where resources will be created"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs where resources will be created"
  type        = list(string)
} 