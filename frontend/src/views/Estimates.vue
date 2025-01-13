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
        <div class="average-label">days average</div>
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
          <div class="member-estimate">{{ member.estimate }} days</div>
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
            <span class="estimate-value">{{ selectedMember?.estimate }} days</span>
          </div>
          <div class="mt-4">
            <div class="justification-label">Justification:</div>
            <div class="justification-text">
              {{ selectedMember?.justification || 'No justification provided.' }}
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Avatar styles available in DiceBear
const avatarStyles = [
  'adventurer',
  'adventurer-neutral',
  'avataaars',
  'avataaars-neutral',
  'big-ears',
  'big-ears-neutral',
  'big-smile',
  'bottts',
  'bottts-neutral',
  'croodles',
  'croodles-neutral',
  'fun-emoji',
  'icons',
  'identicon',
  'initials',
  'lorelei',
  'lorelei-neutral',
  'micah',
  'miniavs',
  'notionists',
  'notionists-neutral',
  'open-peeps',
  'personas',
  'pixel-art',
  'pixel-art-neutral',
  'shapes',
  'thumbs'
]

const currentAvatarStyle = ref('adventurer')
const currentStyleIndex = ref(0)

// Mock team data
interface TeamMember {
  id: number
  name: string
  title: string
  estimate: number
  avatarUrl: string
  justification?: string
}

const mockTeamEstimates = ref<TeamMember[]>([
  {
    id: 1,
    name: 'Sarah Chen',
    title: 'Senior Developer Lead',
    estimate: 15,
    avatarUrl: '',
    justification: 'Need to account for integration testing and security review. Previous similar features took around 2 weeks.'
  },
  {
    id: 2,
    name: 'Jamie Lee',
    title: 'Junior QA Analyst',
    estimate: 7,
    avatarUrl: '',
    justification: 'Based on test coverage requirements and new test cases needed.'
  },
  {
    id: 3,
    name: 'Alex Thompson',
    title: 'Senior Developer',
    estimate: 9,
    avatarUrl: '',
    justification: 'Complex backend changes required. Need to refactor existing code.'
  },
  {
    id: 4,
    name: 'Michael Rodriguez',
    title: 'Senior QA Analyst',
    estimate: 5,
    avatarUrl: '',
    justification: 'Mostly regression testing needed, automation scripts can be reused.'
  },
  {
    id: 5,
    name: 'Emily Parker',
    title: 'Mid-level Developer',
    estimate: 7,
    avatarUrl: '',
    justification: 'Frontend changes are straightforward but need time for proper unit tests.'
  },
  {
    id: 6,
    name: 'David Kim',
    title: 'UX Designer',
    estimate: 6,
    avatarUrl: '',
    justification: 'Need to create and validate new interaction patterns with users.'
  },
  {
    id: 7,
    name: 'Lisa Wang',
    title: 'Backend Developer',
    estimate: 12,
    avatarUrl: '',
    justification: 'Database schema changes and API modifications required.'
  },
  {
    id: 8,
    name: 'Marcus Johnson',
    title: 'DevOps Engineer',
    estimate: 8,
    avatarUrl: '',
    justification: 'Need to update deployment pipeline and add new monitoring.'
  }
])

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

// Calculate average estimate
const averageEstimate = computed(() => {
  const total = mockTeamEstimates.value.reduce((sum, member) => sum + member.estimate, 0)
  return (total / mockTeamEstimates.value.length).toFixed(1)
})

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
    const seed = Math.random().toString(36).substring(7)
    member.avatarUrl = `https://api.dicebear.com/7.x/${currentAvatarStyle.value}/svg?seed=${seed}`
  })
  initializePositions()
}

// Cycle through avatar styles
const cycleAvatarStyle = () => {
  currentStyleIndex.value = (currentStyleIndex.value + 1) % avatarStyles.length
  currentAvatarStyle.value = avatarStyles[currentStyleIndex.value]
  regenerateAvatars()
}

// Add these refs for dialog control
const showDialog = ref(false)
const selectedMember = ref<TeamMember | null>(null)

// Update the showMemberDetails function
const showMemberDetails = (member: TeamMember) => {
  selectedMember.value = member
  showDialog.value = true
}

// Initialize avatars on mount
onMounted(() => {
  regenerateAvatars()
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

.justification-label {
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.justification-text {
  line-height: 1.5;
  color: var(--v-medium-emphasis-opacity);
}

.back-button-container {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 10;
}
</style> 