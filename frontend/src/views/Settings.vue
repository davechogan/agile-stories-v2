<template>
  <div class="settings-container">
    <h1 class="page-title">Settings</h1>
    
    <div class="settings-section">
      <h2 class="section-title">Estimation Settings</h2>
      <div class="settings-content">
        <v-switch
          v-model="settings.useStoryPoints"
          label="Use Story Points"
          color="primary"
        />
        <v-switch
          v-model="settings.useDevDays"
          label="Use Dev Days"
          color="primary"
        />
        
        <v-text-field
          v-model="settings.defaultConfidenceThreshold"
          label="Default Confidence Threshold"
          type="number"
          min="0"
          max="100"
          suffix="%"
        />
      </div>
    </div>
    
    <div class="settings-section">
      <h2 class="section-title">Estimation Roles</h2>
      <div class="settings-content">
        <v-checkbox
          v-for="role in settingsStore.availableRoles"
          :key="role.id"
          v-model="settings.selectedRoles"
          :label="role.name"
          :value="role.id"
          color="primary"
        />
      </div>
    </div>
    
    <div class="action-buttons">
      <v-btn
        color="primary"
        @click="saveSettings"
        :loading="saving"
      >
        Save Settings
      </v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSettingsStore } from '@/stores/settingsStore'

const settingsStore = useSettingsStore()
const saving = ref(false)

// Initialize settings from store
const settings = ref({
  useStoryPoints: settingsStore.useStoryPoints,
  useDevDays: settingsStore.useDevDays,
  defaultConfidenceThreshold: settingsStore.defaultConfidenceThreshold,
  selectedRoles: [...settingsStore.selectedRoles]
})

const saveSettings = async () => {
  saving.value = true
  try {
    // Update store with current settings
    settingsStore.$patch({
      useStoryPoints: settings.value.useStoryPoints,
      useDevDays: settings.value.useDevDays,
      defaultConfidenceThreshold: settings.value.defaultConfidenceThreshold,
      selectedRoles: [...settings.value.selectedRoles]
    })
    await settingsStore.saveSettings()
  } catch (error) {
    console.error('Error saving settings:', error)
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  await settingsStore.loadSettings()
  // Update local settings after loading from store
  settings.value = {
    useStoryPoints: settingsStore.useStoryPoints,
    useDevDays: settingsStore.useDevDays,
    defaultConfidenceThreshold: settingsStore.defaultConfidenceThreshold,
    selectedRoles: [...settingsStore.selectedRoles]
  }
})
</script>

<style scoped>
.settings-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.page-title {
  color: #64B5F6;
  font-size: 2rem;
  margin-bottom: 2rem;
}

.settings-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.section-title {
  color: #64B5F6;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}

.settings-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
}
</style> 