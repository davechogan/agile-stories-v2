provider "aws" {
  region = "us-east-1"
}

module "agile_stories" {
  source = "../../"  # Root module

  environment = "prod"
  
  # Production specific configurations
  cors_allowed_origins = ["https://your-domain.com"]  # Strict CORS
  
  # Larger resource configurations for production
  lambda_memory_size = 512
  lambda_timeout    = 60
  
  # Production packages
  analyze_story_package_path  = "../../../backend/dist/analyze_story.zip"
  estimate_story_package_path = "../../../backend/dist/estimate_story.zip"
  get_status_package_path    = "../../../backend/dist/get_status.zip"
  
  # Production monitoring
  alarm_actions = ["arn:aws:sns:us-east-1:123456789012:prod-alerts"]
  
  # Prod environment variables
  openai_api_key = var.openai_api_key  # From environment-specific variables
} 