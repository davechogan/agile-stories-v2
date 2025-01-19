# Adding New Lambda Functions to Terraform

## File Changes Required

### 1. Backend Setup
- [ ] Add Lambda function code to `backend/src/{function_name}/`
- [ ] Update `backend/build.sh` to include new function
- [ ] Test build script creates `package.zip` in function directory

### 2. Terraform Variables
- [ ] Add package path to `environments/dev/terraform.tfvars`:
```hcl
{function_name}_package_path = "../../../../backend/src/{function_name}/package.zip"
```

- [ ] Declare variable in `environments/dev/variables.tf`:
```hcl
variable "{function_name}_package_path" {
  description = "Path to the {function_name} Lambda package"
  type        = string
}
```

- [ ] Add variable to `modules/agile_stories/variables.tf`:
```hcl
variable "{function_name}_package_path" {
  description = "Path to the {function_name} Lambda package"
  type        = string
}
```

### 3. Module Configuration
- [ ] Add Lambda resource to `modules/lambda/main.tf`:
```hcl
resource "aws_lambda_function" "{function_name}" {
  filename         = var.{function_name}_package_path
  function_name    = "${var.environment}-agile-stories-{function-name}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "app.lambda_handler"
  source_code_hash = filebase64sha256(var.{function_name}_package_path)
  runtime         = "python3.11"
  timeout         = 30  # Adjust as needed
  memory_size     = 128 # Adjust as needed

  environment {
    variables = {
      DYNAMODB_TABLE = "${var.environment}-agile-stories"
      ENVIRONMENT    = var.environment
    }
  }

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }

  tags = {
    Environment = var.environment
    Project     = "agile-stories"
  }
}

# Add CloudWatch Log Group
resource "aws_cloudwatch_log_group" "{function_name}" {
  name              = "/aws/lambda/${aws_lambda_function.{function_name}.function_name}"
  retention_in_days = var.log_retention_days
}
```

### 4. Variable Passing
- [ ] Pass variable in `environments/dev/main.tf`:
```hcl
module "agile_stories" {
  {function_name}_package_path = var.{function_name}_package_path
  # ... other variables
}
```

- [ ] Pass variable in `modules/agile_stories/main.tf`:
```hcl
module "lambda" {
  {function_name}_package_path = var.{function_name}_package_path
  # ... other variables
}
```

### 5. Testing
- [ ] Run `terraform fmt` to format files
- [ ] Run `terraform validate` to check syntax
- [ ] Run `terraform plan` to verify changes
- [ ] Check for any missing variables or dependencies

## Common Issues
1. Missing variable declarations
2. Incorrect file paths
3. Forgotten CloudWatch log groups
4. Missing environment variables
5. Incorrect handler paths

## Best Practices
1. Follow existing naming conventions
2. Match memory and timeout with similar functions
3. Include all standard tags
4. Add appropriate CloudWatch logging
5. Document any special requirements