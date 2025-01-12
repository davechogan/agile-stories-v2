#!/bin/bash

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${GREEN}=== $1 ===${NC}"
}

# Function to print warnings
print_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

# Function to print errors
print_error() {
    echo -e "${RED}ERROR: $1${NC}"
}

# Check AWS credentials
print_status "Checking AWS credentials"
if ! aws sts get-caller-identity &>/dev/null; then
    print_error "AWS credentials not found or invalid"
    print_warning "Please configure your AWS credentials and try again"
    exit 1
fi

# Initialize Terraform
print_status "Initializing Terraform"
terraform init

# Check if state bucket already exists
BUCKET_NAME="agile-stories-terraform-state"
if aws s3api head-bucket --bucket "$BUCKET_NAME" 2>/dev/null; then
    print_warning "State bucket '$BUCKET_NAME' already exists"
    read -p "Do you want to proceed with existing bucket? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Bootstrap cancelled"
        exit 1
    fi
fi

# Apply Terraform configuration
print_status "Creating bootstrap infrastructure"
terraform apply -auto-approve

# Verify resources
print_status "Verifying resources"

# Check S3 bucket
if aws s3api head-bucket --bucket "$BUCKET_NAME" 2>/dev/null; then
    echo "✓ S3 bucket created successfully"
else
    print_error "Failed to create S3 bucket"
    exit 1
fi

# Check DynamoDB table
if aws dynamodb describe-table --table-name "agile-stories-terraform-locks" &>/dev/null; then
    echo "✓ DynamoDB table created successfully"
else
    print_error "Failed to create DynamoDB table"
    exit 1
fi

print_status "Bootstrap complete!"
echo
echo "Next steps:"
echo "1. Initialize dev environment:"
echo "   cd ../environments/dev"
echo "   terraform init"
echo
echo "2. Apply dev environment:"
echo "   terraform plan"
echo "   terraform apply"
echo
echo "3. When ready, do the same for prod environment" 