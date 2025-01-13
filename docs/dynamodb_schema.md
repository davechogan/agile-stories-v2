# DynamoDB Schema

## Table Name
`${environment}-agile-stories`

## Keys
- Partition Key: `story_id` (String) - UUID
- Sort Key: `version` (String) - Identifies the stage/version

## Versions
1. "ORIGINAL"
   ```json
   {
     "story_id": "uuid",
     "version": "ORIGINAL",
     "content": {
       "title": "string",
       "description": "string",
       "acceptance_criteria": ["string"]
     }
   }
   ```

2. "AGILE_COACH"
   ```json
   {
     "story_id": "uuid",
     "version": "AGILE_COACH",
     "content": {
       "improved_story": {
         "title": "string",
         "description": "string",
         "acceptance_criteria": ["string"]
       },
       "invest_analysis": [...],
       "suggestions": [...]
     }
   }
   ```

3. "SENIOR_DEV"
   ```json
   {
     "story_id": "uuid",
     "version": "SENIOR_DEV",
     "content": {
       "technical_analysis": {...}
     }
   }
   ```

4. "TEAM_ESTIMATES#member_id"
   ```json
   {
     "story_id": "uuid",
     "version": "TEAM_ESTIMATES#member1",
     "content": {
       "estimate": number,
       "justification": "string",
       "role": "string"
     }
   }
   ```

5. "FINAL"
   ```json
   {
     "story_id": "uuid",
     "version": "FINAL",
     "content": {
       "average_estimate": number,
       "team_estimates": [
         {
           "member_id": "string",
           "role": "string",
           "estimate": number
         }
       ]
     }
   }
   ```

All items include timestamps:
- created_at: ISO string
- updated_at: ISO string 