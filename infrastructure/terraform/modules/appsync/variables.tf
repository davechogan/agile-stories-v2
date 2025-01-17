variable "environment" {
  description = "Environment name (dev, prod, etc.)"
  type        = string
}

variable "story_table_name" {
  description = "Name of the DynamoDB table storing story data"
  type        = string
} 