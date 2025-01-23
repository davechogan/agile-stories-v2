# Application Architecture

## Overview
The application follows a serverless architecture using AWS services, with a Vue.js frontend and OpenAI integration for story analysis.

## Components

### Frontend (Vue.js)
- **StoryInput.vue**: Initial user story entry
  - Title input
  - Story description
  - Acceptance criteria management
  - Triggers analysis process

- **AgileReview.vue**: Analysis results and editing
  - Displays improved story elements
  - Allows editing of results
  - Shows INVEST analysis
  - Displays AI suggestions
  - Manages tech review handoff

### Backend Services

#### API Gateway
- RESTful endpoints:
  ```
  POST /stories         # Create new story
  GET /stories/{id}     # Get story by ID
  PUT /stories/{id}     # Update story
  ```

#### Lambda Functions
- **Story Analysis Handler**
  ```python
  def handler(event, context):
      # Parse request
      story_data = json.loads(event['body'])
      
      # Call OpenAI
      analysis = analyze_story(story_data)
      
      # Store in DynamoDB
      store_analysis(story_data['id'], analysis)
      
      return {
          'statusCode': 200,
          'body': json.dumps(analysis)
      }
  ```

#### DynamoDB
- **Stories Table**
  ```
  Primary Key: story_id (String)
  Sort Key: version (String)
  Attributes:
    - content: Map
      - title
      - story
      - acceptance_criteria
    - analysis: Map
      - ImprovedTitle
      - ImprovedStory
      - ImprovedAcceptanceCriteria
      - INVESTAnalysis
      - Suggestions
    - created_at
    - updated_at
    - tenant_id
  ```

### OpenAI Integration

#### Client Implementation
```python
from openai import OpenAI

class StoryAnalyzer:
    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-4-turbo-preview"

    def analyze_story(self, story_data):
        prompt = self._build_prompt(story_data)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an experienced Agile coach..."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return self._parse_response(response)

    def _build_prompt(self, story_data):
        return f"""
        Please analyze this user story:
        Title: {story_data['title']}
        Story: {story_data['story']}
        Acceptance Criteria: {story_data['acceptance_criteria']}
        
        Provide:
        1. Improved title
        2. Improved story using "As a [user], I want [goal], so that [benefit]" format
        3. Enhanced acceptance criteria
        4. INVEST analysis
        5. Suggestions for improvement
        """

    def _parse_response(self, response):
        # Parse OpenAI response into structured format
        return {
            "ImprovedTitle": "...",
            "ImprovedStory": "...",
            "ImprovedAcceptanceCriteria": [...],
            "INVESTAnalysis": [...],
            "Suggestions": [...]
        }
```

## Data Flow
1. User submits story through Vue.js frontend
2. API Gateway receives request
3. Lambda function processes request
4. OpenAI analyzes story
5. Results stored in DynamoDB
6. Frontend retrieves and displays analysis
7. User can edit and send to tech review

## Security
- API Gateway authentication
- Lambda IAM roles
- DynamoDB encryption at rest
- HTTPS for all communications
- Environment variables for sensitive data

## Error Handling
- Frontend validation
- API error responses
- OpenAI timeout handling
- DynamoDB retry logic
- User-friendly error messages

## Performance
- DynamoDB auto-scaling
- Lambda concurrency management
- Frontend caching
- Optimized API calls

## Future Enhancements
- Real-time collaboration
- Multiple AI model support
- Enhanced analytics
- Template management
- Integration with project management tools 