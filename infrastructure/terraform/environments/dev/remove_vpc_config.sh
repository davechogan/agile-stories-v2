#!/bin/bash

# Array of function names
FUNCTIONS=(
    "dev-agile-stories-analyze"
    "dev-agile-stories-analyze-worker"
    "dev-agile-stories-estimate"
    "dev-agile-stories-estimate-worker"
    "dev-agile-stories-status"
    "dev-agile-stories-review"
    "dev-agile-stories-review-worker"
)

# Loop through each function
for func in "${FUNCTIONS[@]}"; do
    echo "Removing VPC config from $func..."
    aws lambda update-function-configuration \
        --function-name "$func" \
        --vpc-config SubnetIds=[],SecurityGroupIds=[]
    
    # Wait a few seconds between updates
    sleep 5
done

echo "Done! Check status of ENIs now."