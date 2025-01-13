variable "openai_api_key" {
  description = "OpenAI API key for production environment"
  type        = string
  sensitive   = true
}

variable "lambda_memory_size" {
  description = "Memory allocation for Lambda functions in MB"
  type        = number
  default     = 512 # Larger for prod
}

variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 60 # Longer for prod
}

variable "log_retention_days" {
  description = "CloudWatch log retention period in days"
  type        = number
  default     = 30 # Longer retention for prod
}

variable "enable_detailed_monitoring" {
  description = "Enable detailed CloudWatch monitoring"
  type        = bool
  default     = true # Detailed monitoring for prod
}

variable "max_message_age_threshold" {
  description = "Maximum age of messages in seconds before alerting"
  type        = number
  default     = 3600 # 1 hour for prod
}

variable "dlq_messages_threshold" {
  description = "Number of messages in DLQ before alerting"
  type        = number
  default     = 1 # Stricter threshold for prod
}

variable "alarm_actions" {
  description = "SNS topic ARNs for alarm notifications"
  type        = list(string)
  default     = ["arn:aws:sns:us-east-1:123456789012:prod-alerts"]
}

variable "cost_monitoring_thresholds" {
  description = "Cost thresholds for different services"
  type = object({
    lambda_monthly_threshold     = number
    sqs_monthly_threshold        = number
    dynamodb_monthly_threshold   = number
    apigateway_monthly_threshold = number
  })
  default = {
    lambda_monthly_threshold     = 100 # Higher limits for prod
    sqs_monthly_threshold        = 50
    dynamodb_monthly_threshold   = 50
    apigateway_monthly_threshold = 50
  }
} 