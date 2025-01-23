variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for VPC Link"
  type        = list(string)
}

variable "cors_allowed_origins" {
  description = "List of allowed origins for CORS"
  type        = list(string)
  default     = ["*"] # Should be restricted in production
}

variable "log_retention_days" {
  description = "Number of days to retain API Gateway logs"
  type        = number
  default     = 30
}

variable "analyze_story_lambda_arn" {
  description = "ARN of the analyze story Lambda function"
  type        = string
}

variable "team_estimate_lambda_arn" {
  description = "ARN of the estimate story Lambda function"
  type        = string
}

variable "get_status_lambda_arn" {
  description = "ARN of the get estimation status Lambda function"
  type        = string
}

variable "analyze_story_lambda_name" {
  description = "Name of the analyze story Lambda function"
  type        = string
}

variable "team_estimate_lambda_name" {
  description = "Name of the estimate story Lambda function"
  type        = string
}

variable "get_status_lambda_name" {
  description = "Name of the get estimation status Lambda function"
  type        = string
}

variable "domain_aliases" {
  description = "List of domain aliases for CORS configuration"
  type        = list(string)
} 

variable "analyze_story_worker_name" {
  description = "Name of the analyze story worker Lambda function"
  type        = string
}

variable "analyze_story_worker_arn" {
  description = "ARN of the analyze story worker Lambda function"
  type        = string
}

variable "technical_review_lambda_arn" {
  description = "ARN of the technical review Lambda function"
  type        = string
}

variable "technical_review_lambda_name" {
  description = "Name of the technical review Lambda function"
  type        = string
}
