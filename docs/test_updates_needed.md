# Lambda Test Updates Needed

## Test Locations
Base path: `/backend/tests/`

## Unit Tests to Update

### 1. analyze_story Lambda
- File: `test_analyze_story.py`
- Updates needed:
  - Test AGILE_COACH_PENDING version creation
  - Verify Step Functions workflow input
  - Mock SSM parameter store calls
  - Test error handling scenarios
  - Add integration test with DynamoDB local

### 2. analyze_story_worker Lambda
- File: `test_analyze_story_worker.py`
- Updates needed:
  - Test OpenAI integration (when implemented)
  - Verify version progression (AGILE_COACH_PENDING → AGILE_COACH)
  - Test content preservation between versions
  - Mock DynamoDB interactions

### 3. technical_review Lambda
- File: `test_technical_review.py`
- Updates needed:
  - Test SENIOR_DEV_PENDING version creation
  - Verify Step Functions workflow input
  - Mock SSM parameter store calls
  - Test error handling scenarios
  - Add integration test with DynamoDB local

### 4. technical_review_worker Lambda
- File: `test_technical_review_worker.py`
- Updates needed:
  - Test OpenAI integration (when implemented)
  - Verify version progression (SENIOR_DEV_PENDING → SENIOR_DEV)
  - Test content preservation between versions
  - Mock DynamoDB interactions

### 5. team_estimate Lambda
- File: `test_team_estimate.py`
- Updates needed:
  - Test TEAM_ESTIMATES_PENDING version creation
  - Verify Step Functions workflow input
  - Test team configuration handling
  - Mock SSM parameter store calls
  - Test error handling scenarios
  - Add integration test with DynamoDB local

### 6. team_estimate_worker Lambda
- File: `test_team_estimate_worker.py`
- Updates needed:
  - Test OpenAI integration (when implemented)
  - Test individual estimate generation
  - Test estimate aggregation
  - Verify version progression (TEAM_ESTIMATES_PENDING → FINAL)
  - Test content preservation between versions
  - Mock DynamoDB interactions for both tables

## Integration Tests
- File: `test_integration.py`
- Updates needed:
  - Test complete story flow through all versions
  - Test DynamoDB streams
  - Test Step Functions state transitions
  - Test error recovery scenarios

## Common Test Fixtures
- File: `conftest.py`
- Updates needed:
  - Add mock DynamoDB tables
  - Add mock Step Functions client
  - Add mock SSM client
  - Add sample story data
  - Add OpenAI mock responses

## Test Data
- Directory: `test_data/`
- Updates needed:
  - Add sample stories
  - Add expected OpenAI responses
  - Add Step Functions execution histories
  - Add DynamoDB stream events

## Test Infrastructure
- Directory: `infrastructure/`
- Updates needed:
  - Update LocalStack configuration
  - Add DynamoDB local setup
  - Add Step Functions local setup

## Test Documentation
- Add test coverage requirements
- Document test data structure
- Add test run instructions
- Document mocking strategy
- Add CI/CD test configuration

## Test Automation
- Update GitHub Actions workflow
- Add pre-commit hooks for tests
- Configure test reporting
- Set up test coverage monitoring

## Priority Order
1. Unit tests for each Lambda
2. Integration tests for version flow
3. Infrastructure tests
4. OpenAI integration tests
5. Performance tests
6. Error scenario tests 