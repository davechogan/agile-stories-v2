variable "openai_api_key" {
  description = "OpenAI API key for development environment"
  type        = string
  sensitive   = true
}

variable "lambda_memory_size" {
  description = "Memory allocation for Lambda functions in MB"
  type        = number
  default     = 256 # Smaller for dev
}

variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 30 # Shorter for dev
}

variable "log_retention_days" {
  description = "CloudWatch log retention period in days"
  type        = number
  default     = 7 # Shorter retention for dev
}

variable "enable_detailed_monitoring" {
  description = "Enable detailed CloudWatch monitoring"
  type        = bool
  default     = false # Basic monitoring for dev
}

variable "max_message_age_threshold" {
  description = "Maximum age of messages in seconds before alerting"
  type        = number
  default     = 7200 # 2 hours for dev
}

variable "dlq_messages_threshold" {
  description = "Number of messages in DLQ before alerting"
  type        = number
  default     = 5 # Higher threshold for dev
} 