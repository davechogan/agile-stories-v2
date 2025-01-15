#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting deployment process..."

# Ensure we're in the correct directory
cd "$(dirname "$0")"

echo "📦 Creating fresh package directory..."
rm -rf package/
mkdir package

echo "📥 Installing dependencies..."
pip install --target ./package -r requirements.txt

echo "📄 Copying source files..."
cp app.py ./package/

echo "🗜️ Creating deployment package..."
cd package
zip -r ../function.zip ./*
cd ..

echo "☁️ Deploying to AWS Lambda..."
aws lambda update-function-code \
  --function-name dev-agile-stories-analyze-worker \
  --zip-file fileb://function.zip

echo "✅ Deployment complete!"

# Optional: Clean up
echo "🧹 Cleaning up..."
rm -rf package/
rm function.zip

echo "✨ All done!"
