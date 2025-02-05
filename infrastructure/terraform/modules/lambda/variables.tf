variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for Lambda functions"
  type        = list(string)
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

variable "log_retention_days" {
  description = "Number of days to retain Lambda CloudWatch logs"
  type        = number
  default     = 30
}

variable "lambda_memory_size" {
  description = "Memory size for Lambda functions in MB"
  type        = number
  default     = 256
}

variable "lambda_timeout" {
  description = "Timeout for Lambda functions in seconds"
  type        = number
  default     = 30
}

variable "additional_policy_arns" {
  description = "List of additional IAM policy ARNs to attach to the Lambda role"
  type        = list(string)
  default     = []
}

variable "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table"
  type        = string
}

variable "aws_region" {
  description = "AWS region for the resources"
  type        = string
  default     = "us-east-1"
}

variable "account_id" {
  description = "AWS account ID"
  type        = string
}

variable "stories_table_name" {
  description = "Name of the stories DynamoDB table"
  type        = string
}

variable "stories_table_arn" {
  description = "ARN of the stories DynamoDB table"
  type        = string
}

variable "stories_table_stream_arn" {
  description = "Stream ARN of the stories DynamoDB table"
  type        = string
}

variable "estimations_table_name" {
  description = "Name of the DynamoDB estimations table"
  type        = string
}

variable "estimations_table_arn" {
  description = "ARN of the DynamoDB estimations table"
  type        = string
}

variable "estimations_table_stream_arn" {
  description = "Stream ARN of the estimations DynamoDB table"
  type        = string
}

variable "estimations_role_index_name" {
  description = "Name of the role-story GSI on estimations table"
  type        = string
}

variable "tenant_index_name" {
  description = "Name of the tenant GSI for DynamoDB tables"
  type        = string
}

variable "terraform_locks_table_arn" {
  description = "ARN of the terraform locks DynamoDB table"
  type        = string
}

variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  type        = string
}

variable "analysis_queue_url" {
  description = "URL of the SQS queue for analysis"
  type        = string
}

variable "error_sns_topic_arn" {
  description = "ARN of the error notification SNS topic"
  type        = string
}

variable "error_handler_package_path" {
  description = "Path to the deployment package for the error handler Lambda function"
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

variable "environment_variables" {
  description = "Environment variables for the Lambda function"
  type        = map(string)
  default     = {}
}

variable "attach_policy_statements" {
  description = "Whether to attach additional policy statements"
  type        = bool
  default     = false
}

variable "policy_statements" {
  description = "Map of policy statements to attach to the Lambda role"
  type        = map(any)
  default     = {}
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
