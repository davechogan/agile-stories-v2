export const mockAnalysisResult = {
  ImprovedTitle: "User Authentication: Build Login Page",
  ImprovedStory: "As a user, I want to log in to the application using my username and password so that I can access personalized features securely.",
  ImprovedAcceptanceCriteria: [
    "User can input a valid username and password.",
    "System validates credentials against the database.",
    "Error messages are displayed for invalid credentials.",
    "Login session persists for the duration of user activity or until logout."
  ],
  INVESTAnalysis: {
    I: {
      letter: "I",
      title: "Independent",
      content: "This story is independent as it focuses solely on user authentication."
    },
    N: {
      letter: "N",
      title: "Negotiable",
      content: "The implementation details can be negotiated, such as the design of error messages or session persistence."
    },
    V: {
      letter: "V",
      title: "Valuable",
      content: "The story provides clear value by enabling secure access to user-specific features."
    },
    E: {
      letter: "E",
      title: "Estimable",
      content: "The story is estimable because it requires standard practices for authentication."
    },
    S: {
      letter: "S",
      title: "Small",
      content: "The story is small and focused on a single functionality: login."
    },
    T: {
      letter: "T",
      title: "Testable",
      content: "The story is testable by verifying the inputs, outputs, and system behavior for valid and invalid credentials."
    }
  },
  Suggestions: [
    "Consider defining the maximum character length for username and password inputs.",
    "Add criteria for password recovery or account lockout after multiple failed attempts."
  ]
} 