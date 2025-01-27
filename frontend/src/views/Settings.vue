<template>
  <div class="settings-container">
    <!-- Add debug info -->
    <div class="debug-info" style="position: fixed; top: 10px; left: 10px; background: rgba(0,0,0,0.8); padding: 10px; border-radius: 4px;">
      <div>Current Store Settings:</div>
      <div>estimateType: {{ settingsStore.estimateType }}</div>
      <div>useDevDays: {{ settingsStore.useDevDays }}</div>
      <div>useStoryPoints: {{ settingsStore.useStoryPoints }}</div>
      <div>Radio Value: {{ estimationType }}</div>
    </div>

    <h1 class="page-title">Settings</h1>
    
    <div class="settings-section">
      <h2 class="section-title">Estimation Settings</h2>
      <div class="settings-content">
        <v-card class="mb-4 pa-4">
          <h3>Estimation Units</h3>
          <v-radio-group v-model="estimationType">
            <v-radio
              label="Story Points"
              value="points"
              @change="updateEstimationType('points')"
            ></v-radio>
            <v-radio
              label="Dev Days"
              value="days"
              @change="updateEstimationType('days')"
            ></v-radio>
          </v-radio-group>
        </v-card>
        
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
import { useRouter } from 'vue-router'

const settingsStore = useSettingsStore()
const saving = ref(false)
const router = useRouter()

// Initialize settings from store
const settings = ref({
  useStoryPoints: settingsStore.useStoryPoints,
  useDevDays: settingsStore.useDevDays,
  defaultConfidenceThreshold: settingsStore.defaultConfidenceThreshold,
  selectedRoles: [...settingsStore.selectedRoles]
})

const estimationType = ref(settingsStore.useDevDays ? 'days' : 'points')

const updateEstimationType = (type: string) => {
  settingsStore.useDevDays = type === 'days'
  settingsStore.useStoryPoints = type === 'points'
}

const saveSettings = async () => {
  saving.value = true
  try {
    // Log the values before saving
    console.log('Before save - useStoryPoints:', settings.value.useStoryPoints)
    console.log('Before save - useDevDays:', settings.value.useDevDays)
    console.log('Before save - estimationType:', estimationType.value)
    
    // Update store with current settings
    settingsStore.$patch({
      useStoryPoints: estimationType.value === 'points',
      useDevDays: estimationType.value === 'days',
      estimateType: estimationType.value === 'points' ? 'story_points' : 'person_days'
    })

    // Log the store values after patching
    console.log('After patch - Store values:', {
      useStoryPoints: settingsStore.useStoryPoints,
      useDevDays: settingsStore.useDevDays,
      estimateType: settingsStore.estimateType
    })

    await settingsStore.saveSettings()
  } catch (error) {
    console.error('Error saving settings:', error)
  } finally {
    saving.value = false
  }
}

const goBack = () => {
  router.back()
}

const closePage = () => {
  router.push('/') // Or wherever you want the close button to take you
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