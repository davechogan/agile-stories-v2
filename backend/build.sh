#!/bin/bash

# Build each Lambda function
for func in analyze_story analyze_story_worker technical_review technical_review_worker team_estimate team_estimate_worker story_state_handler workflow_signal_handler; do
    echo "Building $func..."
    cd src/$func
    # Remove old package.zip
    rm -f package.zip
    # Create new package.zip
    zip -r package.zip ./*
    cd ../..
    echo "Built $func/package.zip"
done

echo "Build complete!" 