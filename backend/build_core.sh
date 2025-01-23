#!/bin/bash

# Get the absolute path to the backend directory
BACKEND_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

FUNCTIONS=(
    "analyze_story:dev-agile-stories-analyze"
    "technical_review:dev-agile-stories-review"
)

for func in "${FUNCTIONS[@]}"; do
    IFS=':' read -r -a array <<< "$func"
    FUNCTION_NAME="${array[0]}"
    LAMBDA_NAME="${array[1]}"
    
    echo "Building $FUNCTION_NAME..."
    
    # Create a clean build directory
    BUILD_DIR="/tmp/lambda_build_$FUNCTION_NAME"
    rm -rf "$BUILD_DIR"
    mkdir -p "$BUILD_DIR"
    
    # Copy only necessary files
    cp "$BACKEND_DIR/src/$FUNCTION_NAME/"*.py "$BUILD_DIR/"
    cp "$BACKEND_DIR/src/$FUNCTION_NAME/"*.md "$BUILD_DIR/" 2>/dev/null || true
    
    # Install core dependencies first
    pip install \
        --platform manylinux2014_x86_64 \
        --implementation cp \
        --python-version 3.11 \
        --only-binary=:all: \
        --target "$BUILD_DIR" \
        requests==2.31.0 \
        urllib3==1.26.18
    
    # Then install project dependencies
    pip install \
        --platform manylinux2014_x86_64 \
        --implementation cp \
        --python-version 3.11 \
        --only-binary=:all: \
        --target "$BUILD_DIR" \
        -r "$BACKEND_DIR/src/$FUNCTION_NAME/requirements.txt"
    
    # Create zip
    cd "$BUILD_DIR"
    zip -r package.zip .
    mv package.zip "$BACKEND_DIR/src/$FUNCTION_NAME/"
    cd "$BACKEND_DIR"
    
    # Deploy
    aws lambda update-function-code \
        --function-name "$LAMBDA_NAME" \
        --zip-file "fileb://$BACKEND_DIR/src/$FUNCTION_NAME/package.zip"
    
    # Clean up
    rm -rf "$BUILD_DIR"
    
    echo "Deployed $FUNCTION_NAME"
done 