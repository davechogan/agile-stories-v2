output "api_endpoint" {
  value       = aws_appsync_graphql_api.story_api.uris["GRAPHQL"]
  description = "The GraphQL endpoint URL"
}

output "api_key" {
  value       = aws_appsync_api_key.story_api_key.key
  sensitive   = true
  description = "The API key for AppSync authentication"
}

output "api_id" {
  value       = aws_appsync_graphql_api.story_api.id
  description = "The ID of the AppSync API"
} 