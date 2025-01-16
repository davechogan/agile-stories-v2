output "state_machine_arn" {
  description = "ARN of the Step Functions state machine"
  value       = aws_sfn_state_machine.state_machine.arn
}

output "role_arn" {
  description = "ARN of the IAM role for Step Functions"
  value       = aws_iam_role.step_function_role.arn
}

output "workflow_arn" {
  description = "ARN of the Story Refinement Step Functions workflow"
  value       = aws_sfn_state_machine.state_machine.arn
}
