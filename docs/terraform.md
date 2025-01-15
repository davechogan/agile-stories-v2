# Terraform Infrastructure Documentation

## Overview
The infrastructure for Agile Stories is managed using Terraform, with a modular structure that separates core application resources from environment-specific configurations.

## Environment Structure
- **Region**: us-east-1
- **Environment**: dev
- **VPC**: AgileStoryAppVPC (vpc-075ca467a1d924c87)
  - CIDR: 10.0.0.0/16
  - Public Subnets: 10.0.101.0/24, 10.0.102.0/24
  - Private Subnets: 10.0.103.0/24, 10.0.104.0/24

## Core Resources
### Regional Services
- **DynamoDB Tables**
  - `dev-agile-stories`: Main stories table
  - `dev-agile-stories-estimations`: Estimations table
  
- **SQS Queues**
  - `dev-agile-stories-analysis`: Standard queue for analysis
  - `dev-agile-stories-estimation.fifo`: FIFO queue for estimations

### VPC Resources
- **Lambda Functions** (running in private subnets)
  - analyze-story
  - analyze-story-worker
  - team-estimate
  - team-estimate-worker
  - technical-review
  - technical-review-worker
  - get-status

- **API Gateway**
  - VPC Link for private API access
  - Security groups for VPC access control

## Module Structure
```
infrastructure/terraform/
├── environments/
│   └── dev/
│       ├── main.tf          # Main configuration
│       ├── variables.tf     # Input variables
│       ├── outputs.tf       # Output values
│       └── terraform.tfvars # Environment values
└── modules/
    ├── agile_stories/      # Main application module
    ├── api_gateway/        # API Gateway resources
    ├── dynamodb/          # Database tables
    ├── lambda/            # Lambda functions
    ├── sqs/              # Queue resources
    └── vpc/              # Network resources
```

## Environment Separation
- Each environment (dev/prod) uses:
  - Separate VPC
  - Different CIDR ranges
  - Isolated security groups
  - Regional services with environment prefixes

## Security
- Lambda functions run in private subnets
- API Gateway uses VPC Link
- Security groups control access between services
- DynamoDB and SQS accessed via VPC Endpoints

## Future Considerations
- Production environment setup
- Backup and restore procedures
- Monitoring and alerting configuration 