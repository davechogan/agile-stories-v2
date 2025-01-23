import { defineStore } from 'pinia'

export const useStoryStore = defineStore('story', {
  state: () => ({
    story_id: null,
    token: null
  }),

  actions: {
    setStory(story_id, token) {
      this.story_id = story_id
      this.token = token
    },

    clear() {
      this.story_id = null
      this.token = null
    }
  }
}) 