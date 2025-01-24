export const mockTechReviewData = {
  storyId: 'story123',
  techReviewToken: 'tech-review-token-123',
  status: 'TECH_REVIEW_IN_PROGRESS',
  // ... tech review data
}

export const mockTechReviewResult = {
  improved_story: {
    text: "As a QA Engineer, I want to automate repeated test cases to ensure consistent testing with less manual effort",
    acceptance_criteria: [
      "Automated tests cover all specified test cases.",
      "Automated tests can be triggered manually or on a schedule.",
      "Test results are recorded and easy to review."
    ]
  },
  implementation_details: {
    Frontend: [
      "Create test configuration UI",
      "Add test execution status dashboard",
      "Implement real-time test results viewer",
      "Add test scheduling interface"
    ],
    Backend: [
      "Set up test runner service",
      "Create test result storage API",
      "Implement test scheduling system",
      "Add test report generation"
    ],
    Database: [
      "Design test results schema",
      "Create test configuration tables",
      "Add indexes for quick result retrieval"
    ]
  },
  technical_analysis: {
    Feasibility: {
      Score: 8,
      Description: "Implementation is straightforward with existing test framework. Minor updates needed for scheduling."
    },
    Complexity: {
      Score: 6,
      Description: "Moderate complexity due to scheduling and real-time result tracking requirements."
    },
    Dependencies: {
      Score: 7,
      Description: "Good maintainability with proper test organization and documentation."
    }
  },
  risks_and_considerations: [
    {
      Classification: "Performance",
      Severity: "High",
      Description: "Large test suites might impact execution time",
      PotentialSolution: "Implement parallel test execution and result batching"
    },
    {
      Classification: "Reliability",
      Severity: "Medium",
      Description: "Test environment stability could affect results",
      PotentialSolution: "Add environment health checks and retry mechanisms"
    },
    {
      Classification: "Scalability",
      Severity: "Low",
      Description: "Growing test suite could strain storage",
      PotentialSolution: "Implement result rotation and archiving strategy"
    }
  ],
  Recommendations: [
    "Start with high-priority test cases for initial automation",
    "Implement detailed logging for debugging failures",
    "Set up monitoring for test execution times",
    "Create documentation for test maintenance procedures"
  ],
  estimated_effort: {
    Frontend: "3 days",
    Backend: "5 days",
    Database: "2 days",
    Total: "10 days"
  }
} 