import { defineStore } from 'pinia'

// Load initial state from localStorage if available
const loadInitialState = () => {
  const savedSettings = localStorage.getItem('agileSettings')
  if (savedSettings) {
    return JSON.parse(savedSettings)
  }
  
  // Default state if nothing in localStorage
  return {
    useStoryPoints: true,
    useDevDays: true,
    defaultConfidenceThreshold: 80,
    selectedRoles: [], // Empty by default, will be set by user selections
    availableRoles: [
      { id: 'database_admin', name: 'Database Administrator' },
      { id: 'devops_engineer', name: 'DevOps Engineer' },
      { id: 'frontend_dev', name: 'Frontend Developer' },
      { id: 'qa_engineer', name: 'QA Engineer' },
      { id: 'scrum_master', name: 'Scrum Master' },
      { id: 'security_expert', name: 'Security Expert' },
      { id: 'ui_designer', name: 'UI Designer' },
      { id: 'senior_dev', name: 'Senior Developer' }
    ]
  }
}

export const useSettingsStore = defineStore('settings', {
  state: () => loadInitialState(),

  actions: {
    async saveSettings() {
      try {
        // Save to localStorage
        localStorage.setItem('agileSettings', JSON.stringify(this.$state))
        console.log('Settings saved to localStorage')
      } catch (error) {
        console.error('Failed to save settings:', error)
        throw error
      }
    },
    
    async loadSettings() {
      try {
        const savedSettings = localStorage.getItem('agileSettings')
        if (savedSettings) {
          this.$patch(JSON.parse(savedSettings))
          console.log('Settings loaded from localStorage')
        }
      } catch (error) {
        console.error('Failed to load settings:', error)
        throw error
      }
    }
  }
}) 