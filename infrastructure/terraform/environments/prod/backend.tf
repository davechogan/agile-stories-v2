terraform {
  backend "s3" {
    bucket         = "agile-stories-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "agile-stories-terraform-locks"
    encrypt        = true
  }
} 