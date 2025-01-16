# Testing Step Functions Flow

## Prerequisites
1. Deploy infrastructure:
   - DynamoDB tables
   - Lambda functions
   - Step Functions state machine
   - API Gateway endpoints

## Test Data
```json
{
  "title": "User Registration Feature",
  "description": "Implement user registration functionality",
  "story": "As a new user, I want to register for an account so that I can access the platform",
  "acceptance_criteria": [
    "Email validation is performed",
    "Password meets security requirements",
    "Confirmation email is sent",
    "Account is created in database"
  ],
  "tenant_id": "test-tenant-001"
}
```

## Test Flow

### 1. Initial Story Submission
```bash
curl -X POST https://your-api-gateway/dev/stories/analyze \
  -H "Content-Type: application/json" \
  -d @test-data.json
```
Expected result:
- DynamoDB: AGILE_COACH_PENDING version created
- Step Functions: New execution started

### 2. Monitor Agile Coach Analysis
```bash
aws dynamodb query \
  --table-name dev-agile-stories \
  --key-condition-expression "story_id = :sid" \
  --expression-attribute-values '{":sid": {"S": "STORY_ID_FROM_STEP_1"}}'
```
Expected versions:
1. AGILE_COACH_PENDING
2. AGILE_COACH

### 3. Submit for Technical Review
```bash
curl -X POST https://your-api-gateway/dev/stories/tech-review \
  -H "Content-Type: application/json" \
  -d '{
    "story_id": "STORY_ID_FROM_STEP_1",
    "tenant_id": "test-tenant-001",
    "content": {
      // Content from AGILE_COACH version with any user edits
    }
  }'
```
Expected result:
- DynamoDB: SENIOR_DEV_PENDING version created
- Step Functions: New execution started

### 4. Monitor Technical Review
Query DynamoDB for versions:
1. SENIOR_DEV_PENDING
2. SENIOR_DEV

### 5. Submit for Team Estimates
```bash
curl -X POST https://your-api-gateway/dev/stories/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "story_id": "STORY_ID_FROM_STEP_1",
    "tenant_id": "test-tenant-001",
    "content": {
      // Content from SENIOR_DEV version with any user edits
    },
    "team_config": {
      "roles": ["frontend", "backend", "qa"]
    }
  }'
```
Expected result:
- DynamoDB: TEAM_ESTIMATES_PENDING version created
- Step Functions: New execution started

### 6. Monitor Final Results
Query both tables:
1. Main stories table for FINAL version
2. Estimates table for individual estimates

## Monitoring Tools

### Step Functions Console
1. Navigate to Step Functions in AWS Console
2. Find execution by story_id
3. Check visual workflow and execution history

### CloudWatch Logs
Monitor Lambda logs:
```bash
aws logs tail /aws/lambda/dev-analyze-story --follow
aws logs tail /aws/lambda/dev-analyze-story-worker --follow
# ... repeat for other functions
```

### DynamoDB Streams
Monitor version progression:
```bash
aws dynamodb-streams describe-stream \
  --stream-arn "YOUR_STREAM_ARN"
```

## Error Scenarios to Test
1. OpenAI API failures
2. DynamoDB throttling
3. Missing required fields
4. Invalid story_id references
5. Concurrent modifications

## Cleanup
```bash
# Delete test data from DynamoDB
aws dynamodb delete-item \
  --table-name dev-agile-stories \
  --key '{"story_id": {"S": "STORY_ID_FROM_STEP_1"}}'

# Delete from estimates table
aws dynamodb delete-item \
  --table-name dev-estimates \
  --key '{"story_id": {"S": "STORY_ID_FROM_STEP_1"}}'
``` 