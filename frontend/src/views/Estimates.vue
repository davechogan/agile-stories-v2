<template>
  <div class="test-estimate">
    <!-- Avatar style controls -->
    <div class="avatar-controls">
      <v-btn-group vertical density="compact">
        <v-btn color="primary" size="small" @click="regenerateAvatars">Regenerate All</v-btn>
        <v-btn color="primary" size="small" @click="cycleAvatarStyle">Change Style</v-btn>
      </v-btn-group>
      <div class="current-style text-secondary">Current Style: {{ currentAvatarStyle }}</div>
    </div>
    
    <!-- Center the circle in viewport -->
    <div class="estimation-circle-container">
      <div class="estimation-circle">
        <!-- Fix the average display in center -->
        <div class="center-circle">
          <div class="average-value">
            {{ averageEstimate }}
            <div class="average-label">days average</div>
            <div class="confidence-label" :class="averageConfidence">
              {{ averageConfidence }} confidence
            </div>
          </div>
        </div>
        
        <div 
          v-for="(member, index) in mockTeamEstimates" 
          :key="member.id"
          class="team-member"
          :style="getPositionStyle(index, mockTeamEstimates.length)"
        >
          {{ console.log('Member data:', member) }}
          <v-avatar
            size="60"
            class="member-avatar"
            @click="showMemberDetails(member)"
          >
            <v-img :src="member.avatarUrl"></v-img>
          </v-avatar>
          <div class="member-info">
            {{ console.log('Role:', member.role) }}
            <div class="member-name">{{ getRoleName(member.role) }}</div>
            <div class="member-title">{{ formatRole(member.role) }}</div>
            <div class="member-estimate" :class="getConfidence(member).toLowerCase()">
              {{ getCurrentEstimate(member) }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Add modal dialog -->
    <v-dialog v-model="showDialog" max-width="400">
      <v-card>
        <v-card-title class="member-dialog-title">
          <v-avatar size="48" class="mr-4">
            <v-img :src="selectedMember?.avatarUrl"></v-img>
          </v-avatar>
          {{ getRoleName(selectedMember?.role) }}
        </v-card-title>
        
        <v-card-text>
          <div class="member-dialog-role">{{ selectedMember?.title }}</div>
          
          <div class="member-dialog-estimate">
            <div class="estimate-row">
              <span class="estimate-label">Estimate:</span>
              <span class="estimate-value">
                {{ selectedMember?.estimates[useStoryPoints.value ? 'story_points' : 'person_days'].value }} 
                {{ useStoryPoints.value ? 'points' : 'days' }}
              </span>
            </div>
            
            <div class="confidence-row">
              <span class="estimate-label">Confidence:</span>
              <span class="estimate-value">
                {{ selectedMember?.estimates[useStoryPoints.value ? 'story_points' : 'person_days'].confidence }}
              </span>
            </div>
          </div>
          
          <div class="mt-4">
            <h3 class="section-title">Justification</h3>
            <p class="justification-text">{{ selectedMember?.justification }}</p>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
    
    <!-- Add back button -->
    <div class="back-button-container">
      <v-btn 
        color="primary"
        @click="router.push(`/tech/${route.params.id}`)"
        class="text-uppercase"
      >
        Back to Tech Review
      </v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { CognitoIdentityCredentials, DynamoDB } from 'aws-sdk'
import { useSettingsStore } from '@/stores/settingsStore'
import { useEstimateStore } from '@/stores/estimateStore'

const route = useRoute()
const router = useRouter()
const isLoading = ref(true)
const error = ref('')
const rawEstimateData = ref(null)
const mockTeamEstimates = ref(null)
const settingsStore = useSettingsStore()
const estimateStore = useEstimateStore()

// Initialize useStoryPoints from settings store or localStorage, defaulting to false (days)
const useStoryPoints = ref(false) // Default to days

// Role display names and titles
const roleDisplayData = {
  'backend_dev': { name: 'Backend Sage', title: 'Backend Developer' },
  'frontend_dev': { name: 'UI Wizard', title: 'Frontend Developer' },
  'devops_engineer': { name: 'Cloud Master', title: 'DevOps Engineer' },
  'qa_engineer': { name: 'Test Oracle', title: 'QA Engineer' },
  'security_expert': { name: 'Security Guardian', title: 'Security Expert' },
  'database_admin': { name: 'Data Keeper', title: 'Database Admin' }
}

interface TeamMember {
  id: string;
  name: string;
  title: string;
  avatarUrl: string;
  estimates: {
    story_points: { value: number; confidence: string; }
    person_days: { value: number; confidence: string; }
  };
  justification: Array<{
    title: string;
    content: string;
  }>;
}

// Avatar styles available in DiceBear
const avatarStyles = [
  'bottts',        // Robots
  'bottts-neutral', // More robots
  'shapes',        // Abstract shapes
  'identicon',     // GitHub-style identicons
  'icons',         // Abstract icons
  'pixel-art',     // Pixel art creatures (non-human)
  'thumbs',        // Abstract thumbprint patterns
]

const currentAvatarStyle = ref('bottts')
const currentStyleIndex = ref(0)

// Initial random positions for animation
const initialPositions = ref(new Map())

const getRandomPosition = () => {
  const randomX = (Math.random() - 0.5) * window.innerWidth
  const randomY = (Math.random() - 0.5) * window.innerHeight
  return { x: randomX, y: randomY }
}

// Initialize random positions when team changes
const initializePositions = () => {
  mockTeamEstimates.value.forEach(member => {
    initialPositions.value.set(member.id, getRandomPosition())
  })
  // Trigger reflow to ensure animation works
  setTimeout(() => {
    initialPositions.value = new Map()
  }, 50)
}

// Calculate circle size based on viewport
const circleStyles = computed(() => {
  const size = Math.min(window.innerWidth * 0.8, 800)
  return {
    width: `${size}px`,
    height: `${size}px`
  }
})

// Calculate position for each team member
const getPositionStyle = (index: number, total: number) => {
  const angle = (index * 360) / total - 90
  const radius = Math.min(window.innerWidth * 0.35, 250) // Responsive radius
  
  const angleInRad = (angle * Math.PI) / 180
  const x = Math.cos(angleInRad) * radius
  const y = Math.sin(angleInRad) * radius
  
  return {
    position: 'absolute',
    left: '50%',
    top: '50%',
    transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`,
    transition: 'all 1s cubic-bezier(0.34, 1.56, 0.64, 1)'
  }
}

// Generate new avatar URLs
const regenerateAvatars = () => {
  mockTeamEstimates.value.forEach(member => {
    const style = avatarStyles[Math.floor(Math.random() * avatarStyles.length)]
    const seed = Math.random().toString(36).substring(7)
    member.avatarUrl = `https://api.dicebear.com/7.x/${style}/svg?seed=${seed}`
  })
  initializePositions()
}

// Cycle through avatar styles
const cycleAvatarStyle = () => {
  currentStyleIndex.value = (currentStyleIndex.value + 1) % avatarStyles.length
  currentAvatarStyle.value = avatarStyles[currentStyleIndex.value]
  mockTeamEstimates.value.forEach(member => {
    const seed = Math.random().toString(36).substring(7)
    member.avatarUrl = `https://api.dicebear.com/7.x/${currentAvatarStyle.value}/svg?seed=${seed}`
  })
  initializePositions()
}

// Add these refs for dialog control
const showDialog = ref(false)
const selectedMember = ref<TeamMember | null>(null)

// Update the showMemberDetails function
const showMemberDetails = (member: TeamMember) => {
  selectedMember.value = member
  showDialog.value = true
}

// Add robust error handling for settings
const initializeSettings = () => {
  try {
    // Try to get from settings store first
    const storeSetting = settingsStore.estimateType
    
    // Then try localStorage
    let localSetting = null
    try {
      localSetting = localStorage.getItem('estimateType')
    } catch (e) {
      console.warn('LocalStorage not available:', e)
    }
    
    // Use store setting, then localStorage, then default to false (days)
    useStoryPoints.value = storeSetting === 'story_points' || 
                          (storeSetting === null && localSetting === 'story_points')
    
    console.log('Estimate type initialized:', useStoryPoints.value ? 'story_points' : 'person_days')
  } catch (error) {
    console.error('Error initializing settings:', error)
    useStoryPoints.value = false // Default to days if anything fails
  }
}

// Call on component mount
onMounted(async () => {
  initializeSettings()
  await fetchEstimateData()
  
  // Store the values right after fetching
  if (averageEstimate.value && averageConfidence.value) {
    estimateStore.setEstimates(averageEstimate.value, averageConfidence.value)
    console.log('Stored in Pinia:', {
      average: estimateStore.averageEstimate,
      confidence: estimateStore.averageConfidence
    })
  }
  
  console.log('Initial values:', {
    average: averageEstimate.value,
    confidence: averageConfidence.value
  })
})

// Watch for changes and update both store and localStorage
watch(useStoryPoints, (newValue) => {
  const estimateType = newValue ? 'story_points' : 'person_days'
  settingsStore.setEstimateType(estimateType)
  localStorage.setItem('estimateType', estimateType)
  console.log('Estimate type changed to:', estimateType)
})

// Make sure all estimate displays use this setting
const getCurrentEstimate = (member: TeamMember) => {
  const estimateType = useStoryPoints.value ? 'story_points' : 'person_days'
  return member.estimates[estimateType].value
}

// Update average estimate computation if needed
const averageEstimate = computed(() => {
  const estimateType = useStoryPoints.value ? 'story_points' : 'person_days'
  const rawAverage = rawEstimateData.value?.averages[estimateType].value || 0
  
  // Round to nearest 0.5
  return Math.round(rawAverage * 2) / 2
})

// Transform raw estimate data into display format
const transformEstimateData = (rawData: any): TeamMember[] => {
  console.log('Raw data received:', rawData);
  
  return rawData.individual_estimates.map((estimate: any, index: number) => {
    console.log('Processing estimate:', estimate);
    
    // Updated roles array to match the exact order from the image
    const roles = [
      'database_admin',
      'devops_engineer',
      'frontend_dev',
      'qa_engineer',
      'scrum_master',
      'security_expert',
      'ui_designer',
      'senior_dev'
    ];
    
    const role = roles[index];
    const roleData = roleDisplayData[role] || {
      name: 'Team Member', 
      title: role
    }
    
    // Generate avatar URL using role as seed
    const style = avatarStyles[Math.floor(Math.random() * avatarStyles.length)]
    const seed = role + Date.now()
    
    return {
      id: role,
      role: role,
      name: roleData.name,
      title: roleData.title,
      avatarUrl: `https://api.dicebear.com/7.x/${style}/svg?seed=${seed}`,
      estimates: estimate.estimates,
      justification: estimate.justification
    }
  })
}

// Log environment variables
console.log('Environment Check:', {
  API_URL: import.meta.env.VITE_API_URL,
  ENVIRONMENT: import.meta.env.VITE_ENVIRONMENT,
  COGNITO_USER_POOL_ID: import.meta.env.VITE_COGNITO_USER_POOL_ID,
  COGNITO_CLIENT_ID: import.meta.env.VITE_COGNITO_CLIENT_ID,
  COGNITO_IDENTITY_POOL_ID: import.meta.env.VITE_COGNITO_IDENTITY_POOL_ID,
  MODE: import.meta.env.MODE,
  BASE_URL: import.meta.env.BASE_URL,
})

const fetchEstimateData = async () => {
  try {
    console.log('Starting fetchEstimateData')
    isLoading.value = true
    const storyId = route.params.id
    console.log('Looking for story_id:', storyId)
    
    // Get credentials directly from Cognito Identity Pool
    const credentials = new CognitoIdentityCredentials({
      IdentityPoolId: import.meta.env.VITE_COGNITO_IDENTITY_POOL_ID
    }, {
      region: 'us-east-1'
    })
    
    await credentials.getPromise()
    
    // Initialize DynamoDB with credentials
    const dynamoDB = new DynamoDB.DocumentClient({
      region: 'us-east-1',
      credentials
    })
    
    // Try query first
    const queryParams = {
      TableName: `${import.meta.env.VITE_ENVIRONMENT}-agile-stories-estimations`,
      KeyConditionExpression: 'estimation_id = :eid AND story_id = :sid',
      ExpressionAttributeValues: {
        ':eid': `${storyId}_FINAL`,
        ':sid': storyId
      }
    }
    
    console.log('Trying query first with params:', JSON.stringify(queryParams, null, 2))
    try {
      const queryResponse = await dynamoDB.query(queryParams).promise()
      console.log('Query response:', queryResponse)
      if (queryResponse.Items && queryResponse.Items.length > 0) {
        rawEstimateData.value = queryResponse.Items[0]
        mockTeamEstimates.value = transformEstimateData(queryResponse.Items[0])
        return
      }
    } catch (queryError) {
      console.error('Query failed:', queryError)
    }
    
    // Fall back to scan if query fails or returns no results
    console.log('Falling back to scan...')
    const scanParams = {
      TableName: `${import.meta.env.VITE_ENVIRONMENT}-agile-stories-estimations`,
      FilterExpression: 'story_id = :sid AND #r = :role',
      ExpressionAttributeNames: {
        '#r': 'r#role'
      },
      ExpressionAttributeValues: {
        ':sid': storyId,
        ':role': 'FINAL'
      }
    }
    
    console.log('Scan params:', JSON.stringify(scanParams, null, 2))
    const scanResponse = await dynamoDB.scan(scanParams).promise()
    console.log('Scan response:', scanResponse)
    
    if (scanResponse.Items && scanResponse.Items.length > 0) {
      rawEstimateData.value = scanResponse.Items[0]
      mockTeamEstimates.value = transformEstimateData(scanResponse.Items[0])
    } else {
      error.value = 'No estimate found for this story'
    }
    
  } catch (err) {
    console.error('Error in fetchEstimateData:', err)
    error.value = 'Failed to load team estimates: ' + err.message
  } finally {
    isLoading.value = false
  }
}

// Get confidence level for current estimate type
const getConfidence = (member: TeamMember) => {
  const estimateType = useStoryPoints.value ? 'story_points' : 'person_days'
  return member.estimates[estimateType].confidence
}

// Instead of generating random names each time, let's create a stable mapping
const roleNames = {
  'database_admin': 'Data Keeper',
  'devops_engineer': 'Cloud Master',
  'frontend_dev': 'UI Wizard',
  'qa_engineer': 'Test Oracle',
  'scrum_master': 'Agile Guide',
  'security_expert': 'Security Guardian',
  'ui_designer': 'Design Master',
  'senior_dev': 'Tech Lead'
}

// Replace the getRandomName function with a stable one
const getRoleName = (role: string) => {
  return roleNames[role] || role
}

const formatRole = (role) => {
  const formattedRoles = {
    'backend_dev': 'Backend Developer',
    'frontend_dev': 'Frontend Developer',
    'devops_engineer': 'DevOps Engineer',
    'qa_engineer': 'QA Engineer',
    'security_expert': 'Security Expert',
    'database_admin': 'Database Admin',
    'ui_designer': 'UI Designer',
    'senior_dev': 'Senior Developer',
    'scrum_master': 'Scrum Master'
  }

  return formattedRoles[role] || role
}

// Update average confidence computation if needed
const averageConfidence = computed(() => {
  const estimateType = useStoryPoints.value ? 'story_points' : 'person_days'
  const rawConfidence = rawEstimateData.value?.averages[estimateType].confidence
  
  // Return the confidence string in lowercase for consistency
  return rawConfidence ? rawConfidence.toLowerCase() : 'medium'
})

// When estimates are calculated
watch([averageEstimate, averageConfidence], ([newEstimate, newConfidence]) => {
  console.log('New estimates:', { newEstimate, newConfidence })
  if (newEstimate && newConfidence) {
    estimateStore.setEstimates(newEstimate, newConfidence)
    console.log('Store after setting:', {
      average: estimateStore.averageEstimate,
      confidence: estimateStore.averageConfidence
    })
  }
})
</script>

<style>
.test-estimate {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar-controls {
  position: fixed;
  bottom: 1.5rem;
  left: 1.5rem;
  z-index: 1000;
  scale: 0.9;
}

.current-style {
  margin-top: 0.3rem;
  font-size: 0.75rem;
  opacity: 0.7;
}

.estimation-circle-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  min-height: calc(100vh - 120px);
  padding-top: 64px; /* Add padding for navbar */
}

.estimation-circle {
  position: relative;
  width: min(90vw, 600px); /* Main circle responsive width */
  height: min(90vw, 600px); /* Main circle responsive height */
  margin: 0 auto;
}

.center-circle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.7);
  border-radius: 50%;
  width: min(25%, 150px);
  height: min(25%, 150px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
}

.average-value {
  color: #64B5F6;
  font-size: 2.5rem;
  text-align: center;
}

.average-label {
  font-size: 1rem;
  color: #ffffff;
  opacity: 0.8;
}

.team-member {
  position: absolute;
  text-align: center;
  transition: all 1s cubic-bezier(0.34, 1.56, 0.64, 1);
  width: 140px; /* Increased from 120px to accommodate longer names */
}

.member-avatar {
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: transform 0.2s;
  background: white;
  opacity: 0;
  animation: fadeIn 0.5s forwards;
  animation-delay: 0.5s;
}

.member-avatar:hover {
  transform: scale(1.1);
}

.member-info {
  font-size: 0.8rem;
  white-space: nowrap;
  color: rgba(255, 255, 255, 0.87);
  text-align: center;
  margin-top: 0.5rem;
}

.member-name {
  font-weight: bold;
  color: rgba(255, 255, 255, 0.87);
  font-size: 0.9rem;
}

.member-title {
  opacity: 0.7;
  font-size: 0.7rem;
  margin: 0.2rem 0;
  color: rgba(255, 255, 255, 0.7);
}

.member-estimate {
  color: #64B5F6;
  font-weight: bold;
  margin-top: 0.3rem;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 960px) {
  .estimation-circle {
    width: min(85vw, 350px);
    height: min(85vw, 350px);
  }

  .team-member {
    width: 100px; /* Reduced width for better mobile fit */
  }

  .member-avatar {
    width: 40px !important;
    height: 40px !important;
  }

  .member-info {
    font-size: 0.7rem;
    margin-top: 0.3rem;
  }

  .member-name {
    font-size: 0.8rem;
    white-space: normal; /* Allow names to wrap */
    line-height: 1.2;
  }

  .member-title {
    font-size: 0.6rem;
  }

  /* Fix button layout at bottom */
  .avatar-controls {
    display: none; /* Hide regenerate/cycle buttons on mobile */
  }

  .back-button-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1rem;
    background: rgba(18, 18, 18, 0.95);
    backdrop-filter: blur(10px);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    z-index: 100;
  }

  .estimation-circle-container {
    padding-bottom: 80px; /* Add space for fixed button */
  }

  /* Adjust center circle for mobile */
  .center-circle {
    width: 90px;
    height: 90px;
  }

  .average-value {
    font-size: 1.5rem;
  }

  .average-label {
    font-size: 0.7rem;
  }
}

/* Additional mobile optimization for very small screens */
@media (max-width: 360px) {
  .estimation-circle {
    width: 80vw;
    height: 80vw;
  }

  .member-avatar {
    width: 32px !important;
    height: 32px !important;
  }
}

.member-dialog-title {
  display: flex;
  align-items: center;
  padding: 1rem;
}

.member-dialog-role {
  color: var(--v-medium-emphasis-opacity);
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.member-dialog-estimate {
  margin-top: 16px;
}

.estimate-row, .confidence-row {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.estimate-label {
  font-weight: 500;
  min-width: 100px;
}

.estimate-value {
  margin-left: 8px;
}

.justification-text {
  white-space: pre-wrap;
  line-height: 1.5;
  margin-top: 8px;
}

.section-title {
  color: var(--v-primary-base);
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.back-button-container {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 10;
}

.member-estimate.high {
  color: #4CAF50;
}

.member-estimate.medium {
  color: #FFC107;
}

.member-estimate.low {
  color: #F44336;
}

.circle-container {
  margin-top: 64px;  /* Matches navbar height */
}

/* If you're using v-container, you could also add a class there */
.estimates-container {
  padding-top: 64px;  /* Matches navbar height */
}

.confidence-label {
  font-size: 0.8rem;
  opacity: 0.8;
}

.confidence-label.high {
  color: #4CAF50;
}

.confidence-label.medium {
  color: #FFC107;
}

.confidence-label.low {
  color: #F44336;
}
</style> 