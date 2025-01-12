terraform {
  backend "s3" {
    bucket         = "agile-stories-terraform-state"
    key            = "dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "agile-stories-terraform-locks"
    encrypt        = true
  }
} 