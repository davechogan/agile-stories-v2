variable "name_prefix" {
  description = "Prefix for naming resources"
  type        = string
}

variable "lambda_arns" {
  description = "List of ARNs for Lambda functions used in the Step Functions workflow"
  type        = list(string)
}

variable "workflow_definition" {
  description = "JSON definition of the Step Functions workflow"
  type        = string
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
}

variable "account_id" {
  description = "AWS Account ID"
  type        = string
}