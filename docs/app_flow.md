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


        status = {
            'story_id': story_id,
            'status': 'IN_PROGRESS',
            'steps': {
                'original': 'ORIGINAL' in versions,
                'agile_coach': 'AGILE_COACH' in versions,
                'senior_dev': 'SENIOR_DEV' in versions,
                'team_estimates': any(v.startswith('TEAM_ESTIMATES#') for v in versions),
                'final': 'FINAL' in versions
            },
            'current_step': 'PENDING'
        }
        
        # Determine current step
        if 'FINAL' in versions:
            status['status'] = 'COMPLETED'
            status['current_step'] = 'COMPLETED'
        elif any(v.startswith('TEAM_ESTIMATES#') for v in versions):
            status['current_step'] = 'TEAM_ESTIMATES'
        elif 'SENIOR_DEV' in versions:
            status['current_step'] = 'TEAM_ESTIMATES_PENDING'
        elif 'AGILE_COACH' in versions:
            status['current_step'] = 'SENIOR_DEV_PENDING'
        elif 'ORIGINAL' in versions:
            status['current_step'] = 'AGILE_COACH_PENDING'




## Flow Updates"

"Story Input" page Recieves User input. Content is a Story. On Analyze button click, the story is sent to the analyze_story lambda.
Analyze_story lambda creates a new story in the DynamoDB database, table name dev-agile-stories, as "ORIGINAL" version and returns the story ID. Sends message via SQS to analyze_story_worker lambda.
Analyze_story_worker lambda recieves the message, retrieves the story from the database, sends it to openai for analysis, and stores the result in DynamoDBas "AGILE_COACH" version.
Get_status is called by "Analysis Results" page and is used to poll with the lambda. It recieves the story ID and retrieves the story from the database, and returns the status of the story. When there is a Version for that story ID of "AGILE_COACH" the story is sent to the "Analysis Results" page.  The user can either edit the story further, or accept it as is, either way when the relevant button is pushed, the story, with its story id, is sent to the technical_review Lambda. 


technical_review lambda store a new version in the DynamoDB called "SENIOR_DEV_PENDING" and then send it via SQS to the technical_review_worker lambda.  The technical_review_worker lambda recieves the message, retrieves the story from the database, sends it to openai for analysis, and stores the result in DynamoDB as "SENIOR_DEV" version.  <polling or new way to get the status of the story?> reacts to version "SENIOR_DEV" and sends the story to the "Tech Review" page.  The user can either edit the story further, or accept it as is, if the Accept button is clicked, the story, with its story id, is sent to ??? and is submitted to DynamoDB with Version as COMPLETED. If the user clicks the button for a Team Estimate, the story id sent to the team_estimate lambda.  Team_estimate lambda creates new version 'TEAM_ESTIMATES_PENDING' and sends SQS message for team_estimate_worker lambda. <<somehwere we need to send number of team members so the worker knows when all estimates have returned>> Team_estimate_worker lambda recieves the message and triggers multiple agents "team members" asynchronously. Each agent/team member sends the story to open ai for estimation. Each agent stores their estimates, in both days and in story points (Fibonacci) and justification in DynamoDB as <<need status>>. When all estimates are recieved they are displayed on the "Estimates" page. 


SHould we have a new table for estimates? could store the story id, team member id, role, estimates, and justification.  We could also store the feedback rating from the User for the average, which would need to be stored somwhere. After the user sees the estimates, they can accept it as a SWAG, or not. When they hit accept, we should go back to the technical review page and now display a new field <<or do we add it as an input when the page is first rendered>>, called SWAG or Team Estimate. It would be a non required field if the field exists always. Reminder - The Senior Dev who does the tech review provides their estimate as well. Sending to the team is an additional,optional step. When the user accepts the story by clicking the accept button, a new version is stored in DynamoDB as "FINAL" version.  

************ Summary and Flow ***********

1. Overview
This SaaS application provides user story refinement and estimation. It is tenant-based: each record in DynamoDB is tagged with a tenantId. The front end is built in Vue.js, and each user action is routed through Amazon API Gateway to invoke AWS Lambda functions (written in Python).

Data is stored in two DynamoDB tables:

dev-agile-stories – For the story’s lifecycle stages (versions/statuses).
dev-estimates – For storing team estimates (days, points, justifications).
Settings Page:

Allows users to configure the roles and number of team members for estimation.
Allows toggling between story points (Fibonacci) or days.
These configurations are passed to the Lambdas for dynamic processing.
2. Detailed Flow
2.1. Story Input Flow
User navigates to “Story Input” (Vue.js)

Enters story details (e.g., title, description, acceptance criteria).
Each request includes a tenantId so the backend knows which tenant is processing the story.
User clicks “Analyze”

The front end sends the story data (and tenantId) via API Gateway to analyze_story Lambda.
analyze_story Lambda

Creates a new item in dev-agile-stories with:
Version = ORIGINAL
tenantId
A generated storyId
Returns storyId to the frontend.
Sends an SQS message to trigger the analyze_story_worker Lambda.
analyze_story_worker Lambda

Consumes the SQS message (storyId, tenantId).
Retrieves the ORIGINAL story from dev-agile-stories.
Uses OpenAI to refine the content.
Updates the same item in dev-agile-stories with Version = AGILE_COACH.
2.2. Displaying Analysis Results
Analysis Results (Vue.js)

Option A: Temporarily polls a get_status Lambda via API Gateway to check if the story’s version is AGILE_COACH.
Option B: Future improvement with real-time notifications (WebSockets, AppSync, etc.).
Once AGILE_COACH is found

The refined story is displayed to the user.
The user can edit the story directly on the page but ultimately has a single button: “Send to Tech Review.”
2.3. Technical Review Flow
When user clicks “Send to Tech Review”

The front end sends the (optionally edited) story to the technical_review Lambda via API Gateway.
technical_review Lambda

Updates the story in dev-agile-stories to Version = SENIOR_DEV_PENDING.
Sends an SQS message to technical_review_worker Lambda.
technical_review_worker Lambda

Consumes the SQS message (storyId, tenantId).
Retrieves the story from dev-agile-stories.
Calls OpenAI for a technical review.
Updates the story in dev-agile-stories with Version = SENIOR_DEV.
Tech Review (Vue.js)

Shows the SENIOR_DEV content when ready.
The user decides:
Accept the story without team estimates → final status is COMPLETE.
Click “Team Estimate” → proceed to the next flow.
2.4. Team Estimation Flow (Optional)
User clicks “Team Estimate”

Front end calls the team_estimate Lambda via API Gateway.
The request includes storyId, tenantId, and relevant Settings (number of team members, roles, points vs. days).
team_estimate Lambda

Updates dev-agile-stories to Version = TEAM_ESTIMATES_PENDING.
Sends an SQS message to team_estimate_worker Lambda, passing the team size/roles.
team_estimate_worker Lambda

Consumes SQS message.
Invokes multiple parallel processes (could be the same Lambda or multiple Lambdas) to represent each team member/role.
Each “member” calls OpenAI with the story content.
Each member’s estimate is saved to dev-estimates:
storyId (partition key)
teamMemberId (sort key)
estimateDays, estimatePoints, justification, tenantId, etc.
Averaging the Estimates

Once all estimates are received, team_estimate_worker (or an aggregator) calculates the average in days and average in points.
This aggregate can be stored back in dev-estimates or appended to dev-agile-stories.
Estimates Page (Vue.js)

Displays each individual estimate, plus the averages.
User can Accept → the system updates dev-agile-stories to Version = FINAL.
Final statuses:

COMPLETE if the user skips team estimates and accepts the tech review.
FINAL if the user completes team estimates and accepts.
3. Data Model
3.1. dev-agile-stories Table
Primary Key: storyId
(Optional) Sort Key: version or you can maintain a single item that you overwrite.
Attributes:
Version (e.g., ORIGINAL, AGILE_COACH, SENIOR_DEV, TEAM_ESTIMATES_PENDING, COMPLETE, FINAL)
storyContent, tenantId, etc.
3.2. dev-estimates Table
Primary Key: storyId
Sort Key: teamMemberId (or role + teamMemberId)
Attributes:
estimateDays, estimatePoints, justification
tenantId, timestamp, etc.
4. Updated Flow Diagram
Below is an ASCII diagram reflecting the integrated approach (API Gateway, multi-tenant data, two-table design):

scss
Copy code
                       ┌───────────────────────┐
         (Vue.js)      │    API Gateway        │
  ┌─────────────────────┴───────────────────────┴──────────────────┐
  │                      Story Input Flow                          │
  │  1) POST /analyze_story  tenantId, story data                  │
  │    └───> analyze_story (Lambda)                                │
  │          [DynamoDB dev-agile-stories: Version=ORIGINAL]        │
  │          → SQS → analyze_story_worker (Lambda)                 │
  │          [Call OpenAI, update Version=AGILE_COACH]             │
  │                                                                │
  │  2) (Analysis Results Page)                                    │
  │     ─ Poll or future push ─> get_status (Lambda)               │
  │     ─ Displays story with Version=AGILE_COACH                  │
  │     ─ Single button “Send to Tech Review”                      │
  │                                                                │
  │  3) POST /technical_review  tenantId, storyId                  │
  │     └───> technical_review (Lambda)                            │
  │           [Version=SENIOR_DEV_PENDING in dev-agile-stories]    │
  │           → SQS → technical_review_worker (Lambda)             │
  │           [Call OpenAI, update Version=SENIOR_DEV]             │
  │                                                                │
  │  4) Tech Review Page                                           │
  │     ─ Shows SENIOR_DEV version                                 │
  │     ─ Accept => Version=COMPLETE  OR  “Team Estimate”          │
  │                                                                │
  │  5) POST /team_estimate  tenantId, storyId, roles, etc.        │
  │     └───> team_estimate (Lambda)                               │
  │           [Version=TEAM_ESTIMATES_PENDING]                     │
  │           → SQS → team_estimate_worker (Lambda)                │
  │           [Parallel AI calls => store data in dev-estimates]   │
  │           [Aggregate => average days & points]                 │
  │                                                                │
  │  6) Estimates Page                                             │
  │     ─ Queries dev-estimates for all members                    │
  │     ─ Displays average days & points                           │
  │     ─ Accept => Version=FINAL in dev-agile-stories            │
  └─────────────────────────────────────────────────────────────────┘
5. Remaining Recommendations (Not Fully Incorporated Above)
Below are future or optional enhancements not explicitly woven into the flow:

AWS Step Functions for Orchestration

Could replace manual SQS orchestration.
Manages retries, error handling, and simplifies state management.
Real-Time Notifications (instead of polling)

Use API Gateway WebSockets, SNS -> WebPush, or AWS AppSync subscriptions for push-based updates when each version is ready.
Monitoring & Observability

Add structured logging, metrics (e.g., CloudWatch Metrics, Datadog).
Implement dashboards for queue depth, Lambda concurrency, etc.
Advanced Security

Use IAM + Cognito for multi-tenant user auth.
Encrypt data at rest and in transit.
Enforce row-level security in DynamoDB.
Additional Config & Secrets Management

Store sensitive settings in AWS Systems Manager Parameter Store or AWS Secrets Manager.
Dynamically load them in Lambdas instead of hardcoding.
Final Note
This document now combines the existing flow you’ve built with the tenant-based API Gateway approach, two-table DynamoDB design, and the distinction between COMPLETE vs. FINAL. The diagram reflects your implemented steps plus the requirements for finalizing the tech review and team estimate flows.

