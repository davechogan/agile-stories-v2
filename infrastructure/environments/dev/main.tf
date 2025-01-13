module "agile_stories" {
  source = "../../"
  
  prefix          = "dev-agile-stories"
  environment     = "dev"
  aws_region      = "us-east-1"
  
  # Lambda environment variables
  lambda_environment_variables = {
    DYNAMODB_TABLE = "dev-agile-stories"
    SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/${data.aws_caller_identity.current.account_id}/dev-agile-stories-analysis.fifo"
  }

  # ... other variables ...
} 