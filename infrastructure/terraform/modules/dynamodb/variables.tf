variable "environment" {
  type        = string
  description = "Environment name (dev, prod, etc.)"
}

variable "enable_point_in_time_recovery" {
  description = "Enable point-in-time recovery for DynamoDB tables"
  type        = bool
  default     = true
}

variable "enable_server_side_encryption" {
  description = "Enable server-side encryption for DynamoDB tables"
  type        = bool
  default     = true
}

variable "enable_stream" {
  description = "Enable DynamoDB Streams"
  type        = bool
  default     = true
}

# New variables for estimates table
variable "estimates_table_name" {
  description = "Name of the estimates table"
  type        = string
  default     = "agile-stories-estimations"
}

variable "tags" {
  description = "Additional tags for the DynamoDB tables"
  type        = map(string)
  default     = {}
} 