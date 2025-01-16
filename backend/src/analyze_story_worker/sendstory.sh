curl -X POST \
  https://2rfr1fecv5.execute-api.us-east-1.amazonaws.com/dev/stories/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "test-tenant-001",
    "content": {
      "title": "User Registration Feature",
      "description": "Implement user registration functionality",
      "story": "As a new user, I want to register for an account so that I can access the platform",
      "acceptance_criteria": [
        "Email validation is performed",
        "Password meets security requirements",
        "Confirmation email is sent",
        "Account is created in database"
      ]
    }
  }'