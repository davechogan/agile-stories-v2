# OpenAI Integration

## Agent Prompts Location
The role definitions and prompts for OpenAI agents are located in:
```
/backend/services/analysis/agents/prompts/
```

## Agent Roles and Functions

### Story Analysis Agent (analyze_story_worker)
- Location: `backend/services/analysis/agents/prompts/agile_coach.txt`
- Role: Acts as an Agile Coach to analyze and improve user stories
- Used in: `analyze_story_worker.py`

### Technical Review Agent (technical_review_worker)
- Location: `backend/services/analysis/agents/prompts/senior_dev.txt`
- Role: Acts as a Senior Developer to provide technical analysis
- Used in: `technical_review_worker.py`

### Team Estimation Agents (team_estimate_worker)
- Location: `backend/services/analysis/agents/prompts/team_member.txt`
- Role: Simulates different team members for story estimation
- Used in: `team_estimate_worker.py`
- Note: This agent adapts its role based on the team_config parameter

## Implementation TODO
When implementing OpenAI functionality:
1. Replace placeholder functions with actual OpenAI calls:
   - `analyze_story()` in analyze_story_worker
   - `perform_technical_review()` in technical_review_worker
   - `generate_team_member_estimate()` in team_estimate_worker

2. Use the role definitions from the prompts directory to:
   - Set the system message for each OpenAI chat completion
   - Maintain consistent agent personalities
   - Ensure standardized response formats

3. Consider implementing:
   - Prompt versioning
   - Response validation
   - Token usage optimization
   - Error handling for API limits 