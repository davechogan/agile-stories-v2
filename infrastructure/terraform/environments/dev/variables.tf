# 1. AWS Configuration Variables
variable "account_id" {
  description = "AWS Account ID"
  type        = string
}

variable "environment" {
  description = "Environment name (e.g., dev, prod)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

# 2. VPC Configuration
variable "vpc_id" {
  description = "VPC ID where resources will be created"
  type        = string
}

variable "cidr_block" {
  description = "CIDR block for VPC"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

# 3. Subnet Configuration
variable "public_subnet_cidrs" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "private_subnet_cidrs" {
  description = "List of private subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.103.0/24", "10.0.104.0/24"]
}

# 4. Lambda Package Paths
variable "analyze_story_package_path" {
  description = "Path to analyze story Lambda package"
  type        = string
}

variable "analyze_story_worker_package_path" {
  description = "Path to analyze story worker Lambda package"
  type        = string
}

variable "team_estimate_package_path" {
  description = "Path to team estimate Lambda package"
  type        = string
}

variable "team_estimate_worker_package_path" {
  description = "Path to team estimate worker Lambda package"
  type        = string
}

variable "technical_review_package_path" {
  description = "Path to technical review Lambda package"
  type        = string
}

variable "technical_review_worker_package_path" {
  description = "Path to technical review worker Lambda package"
  type        = string
}

variable "get_status_package_path" {
  description = "Path to get status Lambda package"
  type        = string
}

# 5. API Configuration
variable "openai_api_key" {
  description = "OpenAI API Key (stored in AWS Secrets Manager)"
  type        = string
  default     = ""
} 

variable "error_handler_package_path" {
  description = "Path to error handler Lambda package"
  type        = string
}