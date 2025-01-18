# VPC and Permissions Debugging Session - March 19, 2024

## Initial Problem
During deployment, we encountered two major issues:
1. Security groups appearing to be in the wrong VPC
2. Terraform permissions not working as expected

## VPC Investigation

### Symptoms
- Terraform plan showed security groups trying to move from `vpc-09557185ab87a01df` to `vpc-075ca467a1d924c87`
- All subnets were actually in `vpc-09557185ab87a01df`
- terraform.tfvars had `vpc-075ca467a1d924c87`

### Root Cause
We discovered that terraform.tfvars wasn't being properly referenced before today's changes. When new code started using the tfvars file correctly, it exposed a mismatch between:
- The VPC ID in terraform.tfvars (`vpc-075ca467a1d924c87`)
- The actual VPC where all resources existed (`vpc-09557185ab87a01df`)

### Solution
Updated terraform.tfvars to use the correct VPC ID:
```hcl
vpc_id = "vpc-09557185ab87a01df"  # Changed to match where subnets exist
```

## Permissions Investigation

### Symptoms
- User `agile-stories-v2-terraform` had permissions issues
- Previously working operations started failing
- CloudTrail lookups weren't working

### Root Cause
When adding CloudTrail permissions, we accidentally replaced all existing permissions in the IAM policy instead of adding to them. This happened because:
1. The policy was at version limit
2. Creating a new version replaced all permissions instead of adding to them
3. Only CloudTrail permissions remained in the active version

### Solution
1. Temporarily rolled back to policy version 7 (previous working version)
2. Created new policy version combining all needed permissions:
   - Original permissions from v7
   - CloudTrail permissions
   - Additional service permissions (AppSync, CloudFront, etc.)

## Lessons Learned
1. Always verify VPC/subnet relationships when seeing VPC-related changes
2. Check terraform.tfvars usage and variable precedence
3. When updating IAM policies:
   - Keep track of all required permissions
   - Combine permissions when creating new versions
   - Verify policy contents after updates

## Future Recommendations
1. Document all VPC and subnet relationships
2. Maintain a list of required IAM permissions
3. Consider using terraform workspaces or separate state files for different environments
4. Implement regular policy version cleanup
5. Add automated tests for infrastructure configuration

## Related Resources
- VPC ID: vpc-09557185ab87a01df
- IAM User: arn:aws:iam::784902437693:user/agile-stories-v2-terraform
- IAM Policy: arn:aws:iam::784902437693:policy/Terraform_User_Policies 