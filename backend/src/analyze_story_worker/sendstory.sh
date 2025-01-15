curl -X POST \
  https://2rfr1fecv5.execute-api.us-east-1.amazonaws.com/dev/stories/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Password Reset Feature",
    "description": "Allow users to reset their forgotten passwords securely",
    "story": "As a user, I want to reset my password when I forget it",
    "acceptance_criteria": [
      "Given I am on the login page",
      "When I click forgot password",
      "Then I should receive a reset email"
    ]
  }'