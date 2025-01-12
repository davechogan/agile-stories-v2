# Core infrastructure components
provider "aws" {
  region = var.aws_region
}

# Reference existing VPC
data "aws_vpc" "existing" {
  cidr_block = "10.0.0.0/16"
}

# Get existing subnets
data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.existing.id]
  }
  
  tags = {
    Type = "Private"
  }
}

data "aws_subnets" "public" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.existing.id]
  }
  
  tags = {
    Type = "Public"
  }
}

# API Gateway
module "api_gateway" {
  source = "./modules/api_gateway"
  vpc_id = data.aws_vpc.existing.id
  # ... configuration ...
}

# Lambda Functions
module "lambda_functions" {
  source = "./modules/lambda"
  vpc_id = data.aws_vpc.existing.id
  subnet_ids = data.aws_subnets.private.ids
  # ... configuration ...
}

# SQS Queues
module "queues" {
  source = "./modules/sqs"
  # ... configuration ...
}

# DynamoDB Tables
module "dynamodb" {
  source = "./modules/dynamodb"
  # ... configuration ...
} 