#!/bin/bash

# Build each Lambda function with mapping to actual AWS function names
FUNCTIONS=(
    "analyze_story:dev-agile-stories-analyze"
    "analyze_story_worker:dev-agile-stories-analyze-worker"
    "technical_review:dev-agile-stories-review"
    "technical_review_worker:dev-agile-stories-review-worker"
    "team_estimate:dev-agile-stories-estimate"
    "team_estimate_worker:dev-agile-stories-estimate-worker"
    "story_state_handler:dev-agile-stories-story-state-handler"
    "workflow_signal_handler:dev-agile-stories-workflow-signal-handler"
)

# Debug: Show what we're about to build
echo "Will build these functions:"
for func_pair in "${FUNCTIONS[@]}"; do
    local_name=${func_pair%%:*}
    aws_name=${func_pair#*:}
    echo "- $local_name -> $aws_name"
done

# Confirm before proceeding
read -p "Proceed with build and deploy? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Operation cancelled"
    exit 1
fi

# Build each Lambda function
for func_pair in "${FUNCTIONS[@]}"; do
    local_name=${func_pair%%:*}
    aws_name=${func_pair#*:}
    
    echo "Building $local_name..."
    cd src/$local_name
    # Remove old package.zip
    rm -f package.zip
    # Create new package.zip - just app.py
    zip package.zip app.py > /dev/null
    cd ../..
    echo "Built $local_name/package.zip"
    
    # Deploy the function
    echo "Deploying $local_name as $aws_name..."
    aws lambda update-function-code \
        --no-cli-pager \
        --function-name "$aws_name" \
        --zip-file fileb://src/$local_name/package.zip > /dev/null
    echo "Deployed $local_name"
done

echo "Build and deploy complete!" 