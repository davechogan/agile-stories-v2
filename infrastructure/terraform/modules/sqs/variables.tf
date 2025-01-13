variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
}

variable "message_retention_seconds" {
  description = "Time (in seconds) that messages will be kept in SQS queues"
  type        = number
  default     = 86400 # 1 day
}

variable "visibility_timeout_seconds" {
  description = "Time (in seconds) that messages will be invisible after being received"
  type        = number
  default     = 900 # 15 minutes
}

variable "max_receive_count" {
  description = "Maximum number of times a message can be received before being sent to the DLQ"
  type        = number
  default     = 3
}

variable "dlq_message_retention_seconds" {
  description = "Time (in seconds) that messages will be kept in DLQ"
  type        = number
  default     = 1209600 # 14 days
}

variable "alarm_actions" {
  description = "List of ARNs to notify when alarm triggers (e.g., SNS topics)"
  type        = list(string)
  default     = []
}

variable "ok_actions" {
  description = "List of ARNs to notify when alarm returns to OK state"
  type        = list(string)
  default     = []
}

variable "max_message_age_threshold" {
  description = "Maximum age of messages in seconds before alerting"
  type        = number
  default     = 3600 # 1 hour
}

variable "dlq_messages_threshold" {
  description = "Number of messages in DLQ before alerting"
  type        = number
  default     = 1
}

variable "high_throughput_threshold" {
  description = "Number of messages per 5 minutes that indicates high throughput"
  type        = number
  default     = 1000
}

variable "aws_region" {
  description = "AWS region for the CloudWatch dashboard"
  type        = string
  default     = "us-east-1"
}

variable "dashboard_refresh_interval" {
  description = "Dashboard refresh interval in seconds"
  type        = number
  default     = 300 # 5 minutes
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
    lambda_monthly_threshold     = 10 # USD
    sqs_monthly_threshold        = 5  # USD
    dynamodb_monthly_threshold   = 5  # USD
    apigateway_monthly_threshold = 5  # USD
  }
}

variable "billing_currency" {
  description = "Currency for billing metrics"
  type        = string
  default     = "USD"
}

variable "lambda_function_names" {
  description = "List of Lambda function names for monitoring"
  type        = list(string)
  default     = []
} 