#!/bin/bash

output_file="terraform_diffs.txt"

# Clear the output file if it exists
> "$output_file"

# Array of files to check
files=(
    "infrastructure/terraform/environments/dev/main.tf"
    "infrastructure/terraform/environments/dev/variables.tf"
    "infrastructure/terraform/modules/agile_stories/main.tf"
    "infrastructure/terraform/modules/agile_stories/variables.tf"
    "infrastructure/terraform/modules/lambda/main.tf"
    "infrastructure/terraform/modules/lambda/variables.tf"
    "infrastructure/terraform/modules/api_gateway/main.tf"
    "infrastructure/terraform/modules/api_gateway/variables.tf"
)

# Loop through each file
for file in "${files[@]}"; do
    echo "=== Diff for $file ===" >> "$output_file"
    echo "" >> "$output_file"
    git diff "$file" >> "$output_file"
    echo "" >> "$output_file"
    echo "" >> "$output_file"
done