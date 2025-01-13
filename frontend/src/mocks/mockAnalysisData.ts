export const mockAnalysisResult = {
  original_story: {
    text: "As a user, I want to see a new notification bell icon when I first log in for the day, so that I can be alerted if there is a broadcast message that is relevant to me.",
    acceptance_criteria: [
      "The notification bell icon should only appear on the user's first login of the day.",
      "The notification bell icon should be clearly visible and distinct from other icons.",
      "The notification bell icon should disappear after the user has viewed the broadcast message.",
      "Broadcast messages should be easily readable and accessible from the notification bell icon.",
      "All users should receive broadcast messages simultaneously."
    ],
    context: "",
    version: 1
  },
  improved_story: {
    text: "As a user, I want to see a new notification bell icon when I first log in for the day, so that I can be alerted if there is a broadcast message that is relevant to me.",
    acceptance_criteria: [
      "The notification bell icon should only appear on the user's first login of the day.",
      "The notification bell icon should be clearly visible and distinct from other icons.",
      "The notification bell icon should disappear after the user has viewed the broadcast message.",
      "Broadcast messages should be easily readable and accessible from the notification bell icon.",
      "All users should receive broadcast messages simultaneously."
    ],
    context: "",
    version: 2
  },
  analysis: `INVEST Analysis:
- Independent: The user story is independent, as it does not seem to depend on any other user story for its implementation.
- Negotiable: The story is not very negotiable as it is not clear on what exactly the notification bell should do, or what exactly broadcasting a message entails.
- Valuable: The value to the user is not clearly stated. Why should the user care about this new notification bell?
- Estimable: The story is too vague to be reliably estimated. We don't know what "broadcasting a message" involves.
- Small: The story is not small, as it seems to involve several different features or functionalities.
- Testable: The acceptance criteria are too vague to be testable. What does it mean for everyone to "get it" and "read it"?`,
  suggestions: {
    "Clarity Needed": "We may need to clarify what exactly 'broadcasting a message' involves. Does it mean sending a message to all users, or just some users? Is the message sent in real time, or is it pre-recorded and sent at a specified time?",
    "User Interaction": "We should also clarify what it means for a user to 'get' and 'read' the message. Does the user need to click on the notification bell icon to read the message, or is the message displayed in some other way? What happens after the user has read the message? Is there any sort of confirmation or acknowledgement required from the user?"
  },
  status: "agile_coach_review",
  timestamp: new Date().toISOString()
} 