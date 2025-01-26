# Add data sources at the top of the file
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

# Cognito User Pool
resource "aws_cognito_user_pool" "main" {
  name = "${var.environment}-agile-stories-pool"
  
  # Password policy
  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }
  
  # Allow email sign-in
  username_attributes = ["email"]
  
  # Email verification
  verification_message_template {
    default_email_option = "CONFIRM_WITH_CODE"
  }
  
  # Auto verify email
  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }
  
  # Email verification attribute
  email_verification_message = "Your verification code is {####}"
  email_verification_subject = "Your verification code"
}

# Cognito Identity Pool (for AWS service access)
resource "aws_cognito_identity_pool" "main" {
  identity_pool_name = "${var.environment}-agile-stories-identity"
  
  allow_unauthenticated_identities = true
  
  cognito_identity_providers {
    client_id               = aws_cognito_user_pool_client.main.id
    provider_name           = aws_cognito_user_pool.main.endpoint
    server_side_token_check = false
  }
}

# IAM role for authenticated users
resource "aws_iam_role" "authenticated" {
  name = "${var.environment}-cognito-authenticated"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "cognito-identity.amazonaws.com"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "cognito-identity.amazonaws.com:aud" = aws_cognito_identity_pool.main.id
          }
          "ForAnyValue:StringLike" = {
            "cognito-identity.amazonaws.com:amr": "authenticated"
          }
        }
      }
    ]
  })
}

# Policy for authenticated users to access DynamoDB
resource "aws_iam_role_policy" "authenticated_policy" {
  name = "${var.environment}-authenticated-policy"
  role = aws_iam_role.authenticated.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:Query"
        ]
        Resource = [
          "arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:table/${var.environment}-agile-stories-estimations"
        ]
      }
    ]
  })
}

# Add IAM role for unauthenticated users
resource "aws_iam_role" "unauthenticated" {
  name = "${var.environment}-cognito-unauthenticated"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "cognito-identity.amazonaws.com"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "cognito-identity.amazonaws.com:aud" = aws_cognito_identity_pool.main.id
          }
          "ForAnyValue:StringLike" = {
            "cognito-identity.amazonaws.com:amr": "unauthenticated"
          }
        }
      }
    ]
  })
}

# Update policy for unauthenticated users
resource "aws_iam_role_policy" "unauthenticated" {
  name = "${var.environment}-unauthenticated-policy"
  role = aws_iam_role.unauthenticated.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:Scan",
          "dynamodb:Query"
        ]
        Resource = [
          "arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:table/${var.environment}-agile-stories-estimations"
        ]
      }
    ]
  })
}

# Update the identity pool role attachment
resource "aws_cognito_identity_pool_roles_attachment" "main" {
  identity_pool_id = aws_cognito_identity_pool.main.id
  
  roles = {
    authenticated   = aws_iam_role.authenticated.arn
    unauthenticated = aws_iam_role.unauthenticated.arn
  }
}

# User Pool Client for web app
resource "aws_cognito_user_pool_client" "main" {
  name = "${var.environment}-agile-stories-client"
  
  user_pool_id = aws_cognito_user_pool.main.id
  
  # No client secret for JavaScript applications
  generate_secret = false
  
  # OAuth settings
  allowed_oauth_flows  = ["implicit"]
  allowed_oauth_scopes = ["email", "openid", "profile"]
  callback_urls        = ["https://agile-advisor.com/callback"]
  logout_urls         = ["https://agile-advisor.com"]
} 