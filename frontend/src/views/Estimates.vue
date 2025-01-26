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
    
    <!-- Circle layout with centered average -->
    <div class="estimation-circle" :style="circleStyles">
      <div class="average-estimate">
        <div class="average-number">{{ averageEstimate }}</div>
        <div class="average-label">
          {{ useStoryPoints ? 'story points' : 'days' }} average
        </div>
      </div>
      
      <div 
        v-for="(member, index) in mockTeamEstimates" 
        :key="member.id"
        class="team-member"
        :style="getPositionStyle(index, mockTeamEstimates.length)"
      >
        <v-avatar
          size="60"
          class="member-avatar"
          @click="showMemberDetails(member)"
        >
          <v-img :src="member.avatarUrl"></v-img>
        </v-avatar>
        <div class="member-info">
          <div class="member-name">{{ member.name }}</div>
          <div class="member-title">{{ member.title }}</div>
          <div class="member-estimate" :class="getConfidence(member).toLowerCase()">
            {{ getCurrentEstimate(member) }}
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
          {{ selectedMember?.name }}
        </v-card-title>
        
        <v-card-text>
          <div class="member-dialog-role">{{ selectedMember?.title }}</div>
          <div class="member-dialog-estimate">
            <span class="estimate-label">Estimate:</span>
            <span class="estimate-value">
              {{ selectedMember?.estimates[estimateType].value }} 
              {{ estimateType === 'story_points' ? 'points' : 'days' }}
            </span>
            <div class="confidence-level">
              Confidence: {{ selectedMember?.estimates[estimateType].confidence }}
            </div>
          </div>
          
          <div class="mt-4">
            <div v-for="(section, index) in selectedMember?.justification" 
                 :key="index" 
                 class="justification-section">
              <h3 class="section-title">{{ section.title }}</h3>
              <p class="section-content">{{ section.content }}</p>
            </div>
          </div>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="showDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Add back button -->
    <div class="back-button-container">
      <v-btn 
        color="primary"
        @click="router.push('/tech')"
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

const route = useRoute()
const router = useRouter()
const isLoading = ref(true)
const error = ref('')
const rawEstimateData = ref(null)
const mockTeamEstimates = ref(null)
const useStoryPoints = ref(true)  // Default to story points

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
  const angle = (index * 360) / total - 90 // Start from top
  const radius = 250 // Increased from 200 to 250 for better spacing
  
  // Get initial random position if it exists
  const initialPos = initialPositions.value.get(mockTeamEstimates.value[index].id)
  
  if (initialPos) {
    return {
      position: 'absolute',
      left: `${initialPos.x}px`,
      top: `${initialPos.y}px`,
      transform: 'translate(-50%, -50%)',
      transition: 'none'
    }
  }
  
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

const estimateType = ref('person_days') // or get from settings

// Calculate average based on current estimate type
const averageEstimate = computed(() => {
  const estimateType = useStoryPoints.value ? 'story_points' : 'person_days'
  return rawEstimateData.value?.averages[estimateType].value || 0
})

// Transform raw estimate data into display format
const transformEstimateData = (rawData: any): TeamMember[] => {
  console.log('Raw data received:', rawData);
  
  return rawData.individual_estimates.map((estimate: any) => {
    console.log('Processing estimate:', estimate);
    
    const roleData = roleDisplayData[estimate.role] || {
      name: 'Team Member', 
      title: estimate.role
    }
    
    // Generate avatar URL using role as seed
    const style = avatarStyles[Math.floor(Math.random() * avatarStyles.length)]
    const seed = estimate.role + Date.now()
    
    // Parse justification text into sections
    const justificationText = estimate.justification
    console.log('Justification text:', justificationText);
    
    // Simply split by double newlines and format each section
    const sections = justificationText.split('\n\n').map(section => {
      const lines = section.split('\n')
      return {
        title: lines[0].replace(':', '').trim(),
        content: lines.slice(1).join('\n').trim()
      }
    }).filter(section => section.content); // Only keep sections with content
    
    console.log('Processed sections:', sections);
    
    return {
      id: estimate.role,
      name: roleData.name,
      title: roleData.title,
      avatarUrl: `https://api.dicebear.com/7.x/${style}/svg?seed=${seed}`,
      estimates: {
        story_points: {
          value: estimate.estimates.story_points.value,
          confidence: estimate.estimates.story_points.confidence
        },
        person_days: {
          value: estimate.estimates.person_days.value,
          confidence: estimate.estimates.person_days.confidence
        }
      },
      justification: sections
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
    
    // Get credentials directly from Cognito Identity Pool
    console.log('Getting credentials from Identity Pool')
    const credentials = new CognitoIdentityCredentials({
      IdentityPoolId: import.meta.env.VITE_COGNITO_IDENTITY_POOL_ID
    }, {
      region: 'us-east-1'
    })
    
    await credentials.getPromise()
    console.log('Got credentials:', credentials)
    
    // Initialize DynamoDB with credentials
    const dynamoDB = new DynamoDB.DocumentClient({
      region: 'us-east-1',
      credentials
    })
    
    // Use scan instead of query since we don't have the estimation_id
    const params = {
      TableName: `${import.meta.env.VITE_ENVIRONMENT}-agile-stories-estimations`,
      FilterExpression: 'story_id = :sid AND #r = :role',
      ExpressionAttributeNames: {
        '#r': 'role'
      },
      ExpressionAttributeValues: {
        ':sid': storyId,
        ':role': 'FINAL'
      }
    }
    
    console.log('Scanning DynamoDB with params:', params)
    const response = await dynamoDB.scan(params).promise()
    console.log('DynamoDB response:', response)
    
    if (response.Items && response.Items.length > 0) {
      rawEstimateData.value = response.Items[0]
      mockTeamEstimates.value = transformEstimateData(response.Items[0])
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

// Initialize on mount
onMounted(async () => {
  console.log('Component mounted')
  await fetchEstimateData()
})

// Toggle estimate type display
const toggleEstimateType = () => {
  useStoryPoints.value = !useStoryPoints.value
}

// Get current estimate value for display
const getCurrentEstimate = (member: TeamMember) => {
  const estimateType = useStoryPoints.value ? 'story_points' : 'person_days'
  return member.estimates[estimateType].value
}

// Get confidence level for current estimate type
const getConfidence = (member: TeamMember) => {
  const estimateType = useStoryPoints.value ? 'story_points' : 'person_days'
  return member.estimates[estimateType].confidence
}

// Add error watcher
watch(error, (newError) => {
  if (newError) {
    console.error('Error state updated:', newError)
  }
})
</script>

<style>
.test-estimate {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
  position: relative;
  display: flex;
  flex-direction: column;
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

.estimation-circle {
  position: relative;
  margin: -2rem auto 0;
  padding-top: 2rem;
}

.average-estimate {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  background: rgba(33, 150, 243, 0.1);
  padding: 1rem;
  border-radius: 50%;
  width: 120px;
  height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.average-number {
  font-size: 2rem;
  font-weight: bold;
  color: #64B5F6;
}

.average-label {
  font-size: 0.8rem;
  opacity: 0.87;
  color: rgba(255, 255, 255, 0.87);
}

.team-member {
  position: absolute;
  text-align: center;
  transition: all 1s cubic-bezier(0.34, 1.56, 0.64, 1);
  width: 120px;
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
}

.member-name {
  font-weight: bold;
  color: rgba(255, 255, 255, 0.87);
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

@media (max-width: 768px) {
  .avatar-controls {
    bottom: 1rem;
    left: 1rem;
  }
  
  .current-style {
    font-size: 0.7rem;
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
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.estimate-label {
  font-weight: 500;
}

.estimate-value {
  color: var(--v-theme-primary);
  font-weight: bold;
}

.justification-section {
  margin-top: 1rem;
  padding: 0.5rem 0;
}

.section-title {
  color: var(--v-primary-base);
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.section-content {
  color: var(--v-medium-emphasis-opacity);
  line-height: 1.4;
}

.confidence-level {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: var(--v-medium-emphasis-opacity);
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
</style> 