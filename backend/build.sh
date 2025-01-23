#!/bin/bash

set -e  # Exit on any command failure

# Build each Lambda function with mapping to actual AWS function names
FUNCTIONS=(
    "analyze_story:dev-agile-stories-analyze"
    #"analyze_story_worker:dev-agile-stories-analyze-worker"
    "technical_review:dev-agile-stories-review"
    #"technical_review_worker:dev-agile-stories-review-worker"
    #"team_estimate:dev-agile-stories-estimate"
    #"team_estimate_worker:dev-agile-stories-estimate-worker"
    #"get_status:dev-agile-stories-status"
    #"story_state_handler:dev-agile-stories-story-state-handler"
    #"error_handler:dev-agile-stories-error-handler"
)

DEBUG=true  # Enable/disable debug mode

if [ "$DEBUG" = true ]; then
    set -x  # Enable command tracing
fi

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
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Operation cancelled"
    exit 1
fi

# Build each Lambda function
for func_pair in "${FUNCTIONS[@]}"; do
    local_name=${func_pair%%:*}
    aws_name=${func_pair#*:}

    echo "Building $local_name..."

    # Install dependencies if requirements.txt exists
    if [ -f "src/$local_name/requirements.txt" ]; then
        echo "Installing dependencies for $local_name..."
        
        # Create temporary build directory
        BUILD_DIR="/tmp/lambda_build_$local_name"
        WHEELS_DIR="/tmp/lambda_wheels"
        rm -rf "$BUILD_DIR" "$WHEELS_DIR"
        mkdir -p "$BUILD_DIR"
        
        # Copy Lambda files to build directory
        cp "src/$local_name/"*.py "$BUILD_DIR/"
        cp "src/$local_name/"*.md "$BUILD_DIR/" 2>/dev/null || true
        
        # Create and activate venv
        python3 -m venv "/tmp/build_venv"
        source "/tmp/build_venv/bin/activate"
        
        # Clear pip cache
        pip cache purge
        
        # Download Linux wheels first
        pip download \
            --no-cache-dir \
            --only-binary=:all: \
            --platform manylinux2014_x86_64 \
            --python-version 3.11 \
            --implementation cp \
            --dest "$WHEELS_DIR" \
            --no-deps \
            -r "src/$local_name/requirements.txt"
            
        # Install from downloaded wheels
        pip install \
            --no-index \
            --find-links "$WHEELS_DIR" \
            --target "$BUILD_DIR" \
            --no-deps \
            -r "src/$local_name/requirements.txt"
        
        deactivate
        rm -rf "/tmp/build_venv" "$WHEELS_DIR"
        
        # Create package.zip in lambda directory
        CURRENT_DIR=$(pwd)
        cd "$BUILD_DIR"
        zip -r "$CURRENT_DIR/src/$local_name/package.zip" .
        cd "$CURRENT_DIR"
        
        # Clean up
        rm -rf "$BUILD_DIR"
        
        # Check package size
        PACKAGE_SIZE=$(stat -f%z "src/$local_name/package.zip")
        echo "Package size: $((PACKAGE_SIZE/1024/1024))MB"
        if [ $PACKAGE_SIZE -gt 70000000 ]; then
            echo "Package too large (>70MB)"
            exit 1
        fi

        # Deploy to AWS
        echo "Deploying $local_name as $aws_name..."
        cd "src/$local_name"
        aws lambda update-function-code \
            --no-cli-pager \
            --function-name "$aws_name" \
            --zip-file "fileb://package.zip" > /dev/null || {
                echo "Failed to deploy $local_name"
                exit 1
            }
        cd "$CURRENT_DIR"
    fi
    
    echo "Deployed $local_name"
done

echo "Build and deploy complete!"
