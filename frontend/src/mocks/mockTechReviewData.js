export const mockTechReviewData = {
  storyId: 'story123',
  techReviewToken: 'tech-review-token-123',
  status: 'TECH_REVIEW_IN_PROGRESS',
  // ... tech review data
}

export const mockTechReviewResult = {
  ImprovedTitle: "Notification System Enhancement",
  ImprovedStory: "As a user, I want to receive real-time notifications on my dashboard so that I can stay updated with critical system events.",
  ImprovedAcceptanceCriteria: [
    "Notifications are displayed as a bell icon with a badge for unread messages.",
    "Clicking on the bell icon opens a modal showing recent notifications.",
    "Users can mark notifications as read."
  ],
  ImplementationDetails: {
    Frontend: [
      "Add notification bell component with animation support.",
      "Implement notification state management.",
      "Add session tracking for the first login of the day.",
      "Create notification overlay/modal for message display."
    ],
    Backend: [
      "Extend user session API to track daily logins.",
      "Add broadcast message endpoints.",
      "Implement notification status tracking.",
      "Add message relevancy filtering logic."
    ],
    Database: [
      "Create a 'Notifications' table to store messages.",
      "Add fields for user ID, message content, timestamp, and read/unread status.",
      "Optimize indexing for fast retrieval of unread messages."
    ]
  },
  TechnicalAnalysis: {
    Feasibility: {
      Description: "Implementation is straightforward with the existing notification system. Will require minor updates to the user session tracking.",
      Score: 8
    },
    Complexity: {
      Description: "Moderate complexity due to real-time notification requirements and session management across multiple devices.",
      Score: 6
    },
    Dependencies: {
      Description: "Main dependencies are the notification service and user session service. Both are stable and well-maintained.",
      Score: 7
    }
  },
  RisksAndConsiderations: [
    {
      Classification: "Performance",
      Severity: "High",
      Description: "High message volume could impact message delivery speed.",
      PotentialSolution: "Implement message queuing and batch processing."
    },
    {
      Classification: "Scalability",
      Severity: "Medium",
      Description: "Growing user base could strain database query performance.",
      PotentialSolution: "Implement database indexing and sharding for scalability."
    },
    {
      Classification: "Security",
      Severity: "Critical",
      Description: "Notifications might contain sensitive information.",
      PotentialSolution: "Encrypt notifications and use role-based access controls."
    },
    {
      Classification: "UI/UX",
      Severity: "Informational",
      Description: "The modal may not render correctly on smaller screens.",
      PotentialSolution: "Ensure responsive design is tested across multiple devices."
    }
  ],
  Recommendations: [
    "Add a priority-based notification categorization system.",
    "Test performance with high message loads to avoid delivery delays.",
    "Implement audit logging for notification changes."
  ]
} 