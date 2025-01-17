import { gql } from '@apollo/client/core'

export const STORY_STATUS_SUBSCRIPTION = gql`
  subscription OnStoryStatusChanged($storyId: ID!) {
    onStoryStatusChanged(storyId: $storyId) {
      story_id
      status
      message
      feedback {
        title_feedback
        story_feedback
        acceptance_criteria_feedback
        overall_score
        improvement_suggestions
      }
    }
  }
` 