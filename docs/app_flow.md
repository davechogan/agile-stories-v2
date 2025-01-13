# Agile Stories App Flow

## Input Phase
- Story title, description, acceptance criteria
- Sources:
  - Manual input
  - JIRA integration

## Analysis Phase (Agile Coach Agent)
- Reviews story quality
- Suggests improvements
- Ensures story follows best practices
- Output: Improved story structure

## Technical Review Phase (Senior Dev Agent)
- Assesses technical implications
- Reviews architecture impact
- Identifies technical considerations
- Output: Technical analysis and recommendations

## Estimation Phase (Team View)
- UI Elements:
  - Team members in circular arrangement
  - Individual avatars (randomized/changeable)
  - Name, title, estimate under each avatar
  - Clickable avatars → estimation justification modal
  - Center display:
    - Average estimate
    - "Facilitator" character holding/flipping card
    
## Data Flow
1. Story Input → Agile Coach Analysis
2. Improved Story → Senior Dev Review
3. Technical Analysis → Team Estimation
4. Individual Estimates → Final Average 


***Output from Agile Expert:***

{
  "ImprovedTitle": "Refined title of the story",
  "ImprovedStory": "A detailed and actionable user story in the format: 'As a [role], I want [goal] so that [reason].'",
  "ImprovedAcceptanceCriteria": [
    "Clear and specific acceptance criteria in bullet-point format.",
    "Each criterion should be independently testable."
  ],
}

"INVESTAnalysis": {
  "letter": "I",
  "title": "Independent",
  "content": "This story is independent as it focuses solely on user authentication without dependencies on other features."
},
{
  "letter": "N",
  "title": "Negotiable",
  "content": "The implementation details can be negotiated, such as the design of error messages or session persistence."
},
{
  "letter": "V",
  "title": "Valuable",
  "content": "The story provides clear value by enabling secure access to user-specific features and protecting user data."
},
{
  "letter": "E",
  "title": "Estimable",
  "content": "The story is estimable as it involves standard authentication practices with clear acceptance criteria."
},
{
  "letter": "S",
  "title": "Small",
  "content": "The story is appropriately sized, focusing on core login functionality without scope creep into password recovery or user management."
},
{
  "letter": "T",
  "title": "Testable",
  "content": "Each acceptance criterion is specific and testable, with clear inputs, actions, and expected outcomes."
}



  "Suggestions": [
    "Actionable recommendations for further improvement or considerations.",
    "Tips for refining the story or acceptance criteria."
  ]

***Output from Senior Dev:***
Your output must be structured and clearly broken into the following sections:

Required Response Format (JSON)
{
  "ImprovedTitle": "Refined title of the story",
  "ImprovedStory": "Actionable user story, typically provided by the Agile Expert.",
  "ImprovedAcceptanceCriteria": [
    "Acceptance criteria refined or confirmed from Agile Expert's output."
  ],
  "ImplementationDetails": {
    "Frontend": [
      "Specific tasks or components needed for frontend implementation."
    ],
    "Backend": [
      "Specific tasks or components needed for backend implementation."
    ],
    "Database": [
      "Specific tasks or components needed for database implementation."
    ]
  },
  "TechnicalAnalysis": {
    "Feasibility": {
      "Description": "High-level summary of the overall feasibility.",
      "Score": "1-10"
    },
    "Complexity": {
      "Description": "High-level summary of the overall complexity.",
      "Score": "1-10"
    },
    "Dependencies": {
      "Description": "High-level summary of the overall dependencies.",
      "Score": "1-10"
    }
  },
  "RisksAndConsiderations": [
    {
      "Classification": "Category of the risk or consideration (e.g., Performance, Security, Scalability, etc.)",
      "Severity": "Critical/High/Medium/Low/Informational",
      "Description": "Brief explanation of the risk or consideration.",
      "PotentialSolution": "Suggested solution or mitigation strategy."
    }
  ],
  "Recommendations": [
    "Actionable suggestions for improving the story or addressing identified risks or gaps."
  ]
}

so how this app works is a user inputs a story title, description and acceptance criteria, or it is ingested via an integration with jira. That is then sent to the agile coach to have them analyze and improve the story. It then goes to the Senior Dev, who is like the tech lead/principal engineer/architect, to review the improved story and assess it from a technical perspective.  Once it makes its changes, the story then goes to the team to estimate. THe page layout for the estimation has each member of the team identified in a circle with a fun avatar, that changes each time or on demand, who are all arranged in a circle. Their name, random, title and estimates are displayed beneath their individual circle. If you click on the avatar a modal opens that shows their justification. for their estimate.  In the center of the circle the average is displayed. For fun, maybe we make that a character holding a card and when all estimates are in, they flip the card to show the average. That would be the only place I could see a "facailitator.

Input Phase
User inputs story (title, description, acceptance criteria)
Or JIRA integration provides it
→ Store in DynamoDB as "ORIGINAL" version
Agile Coach Analysis
Reviews story quality
Suggests improvements
Ensures best practices
→ Store in DynamoDB as "AGILE_COACH" version
Senior Dev Review
Assesses technical implications
Reviews architecture impact
→ Store in DynamoDB as "SENIOR_DEV" version
4. Team Estimation
Each team member provides estimate
→ Store in DynamoDB as "TEAM_ESTIMATES#member_id" versions
Calculate average when complete
→ Store final in DynamoDB as "FINAL" version

***Lambda Implementation Flow***
POST /stories/analyze
Takes original story input
Creates "ORIGINAL" version
Sends to Agile Coach agent
Stores "AGILE_COACH" version
POST /stories/technical-review
Takes improved story
Sends to Senior Dev agent
Stores "SENIOR_DEV" version
3. POST /stories/estimate
Takes "SENIOR_DEV" version
Sends to Team agents
Each stores "TEAM_ESTIMATES#member_id"
When all complete, stores "FINAL"
GET /stories/{id}/status
Checks latest version
Returns progress through workflow