# Team Estimation Flow

## Overview
The team estimation process involves multiple components working together to generate and display role-based estimates for user stories.

## Flow
1. **Initiation**
   - User clicks "Get Team Estimate" on story details page
   - POST request sent to API Gateway with:
     - story_id
     - tenant_id
     - settings (selected roles, estimation preferences)

2. **Main Lambda (team_estimate)**
   - Fetches story from DynamoDB
   - Prepares simplified story payload
   - Spawns worker Lambdas for each selected role
   - Collects responses
   - Calculates averages
   - Stores final combined estimate
   - Returns success response

3. **Worker Lambdas (team_estimate_worker)**
   - Each worker:
     - Loads role-specific prompt
     - Generates estimate using OpenAI
     - Stores individual estimate
     - Returns formatted response

4. **Estimates Page**
   - Fetches final estimate using story_id
   - Displays circular visualization with:
     - Individual role estimates
     - Team average in center
     - Detailed justifications in modal

## Data Structures

### API Request (POST /team-estimate)
```json
{
  "story_id": "string",
  "tenant_id": "string",
  "settings": {
    "selectedRoles": ["backend_dev", "frontend_dev", ...],
    "useStoryPoints": boolean
  }
}
```

### Story Payload (to Workers)
```json
{
  "story_id": "string",
  "tenantId": "string",
  "title": "string",
  "story": "string",
  "acceptance_criteria": "string",
  "implementation_details": "string"
}
```

### Individual Role Estimate (DynamoDB)
```json
{
  "estimation_id": "story_123_backend_dev",
  "story_id": "story_123",
  "tenantId": "tenant_456",
  "role": "backend_dev",
  "estimates": {
    "story_points": {
      "value": 8,
      "confidence": "HIGH"
    },
    "person_days": {
      "value": 12,
      "confidence": "MEDIUM"
    }
  },
  "justification": [
    {
      "title": "Technical Complexity",
      "content": "string"
    }
  ],
  "created_at": "timestamp"
}
```

### Final Combined Estimate (DynamoDB)
```json
{
  "estimation_id": "story_123_final",
  "story_id": "story_123",
  "tenantId": "tenant_456",
  "version": "FINAL",
  "created_at": "timestamp",
  "averages": {
    "story_points": {
      "value": 8.5,
      "confidence": "HIGH"
    },
    "person_days": {
      "value": 12.3,
      "confidence": "MEDIUM"
    }
  },
  "individual_estimates": [
    // Array of individual role estimates
  ]
}
```

## DynamoDB Schema

### Estimates Table
- Primary Key: `estimation_id` (string)
- Sort Key: `story_id` (string)
- GSI1: `tenantId-index`
  - Partition Key: `tenantId`
  - Sort Key: `created_at`

## Key Features
- Parallel processing of role estimates
- Both story points and person days estimates
- Confidence levels for all estimates
- Role-specific justifications
- Single-query data retrieval for frontend
- Tenant isolation
- Version tracking for final estimates

## Error Handling
- Worker failures don't block other estimates
- Main Lambda validates all responses
- Frontend handles partial data gracefully
- Timeouts managed by ThreadPoolExecutor 