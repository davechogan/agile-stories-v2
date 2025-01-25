<template>
  <div class="test" :class="{ 'fade-out': isExiting }">
    <div class="two-column-layout">
      <!-- Left Column: Primary Content -->
      <div class="primary-content-wrapper">
        <div class="primary-content">
          <h2 class="page-title">Story Input</h2>
          <div class="story-form">
            <div class="form-group">
              <label class="input-label">Title</label>
              <v-text-field
                v-model="story.title"
                label="Enter a descriptive title"
                variant="outlined"
              />
            </div>

            <div class="form-group">
              <label class="input-label">User Story</label>
              <v-textarea
                v-model="story.text"
                label="As a [user type], I want [goal], so that [benefit]"
                variant="outlined"
                auto-grow
                rows="3"
              />
            </div>

            <div class="form-group">
              <label class="input-label">Acceptance Criteria</label>
              <div class="criteria-list">
                <div v-for="(criteria, index) in story.acceptance_criteria" 
                     :key="index"
                     class="criteria-item">
                  <v-textarea
                    v-model="story.acceptance_criteria[index]"
                    variant="outlined"
                    auto-grow
                    rows="1"
                  />
                  <v-btn 
                    icon="mdi-delete" 
                    size="small"
                    color="error" 
                    variant="text"
                    @click="removeCriteria(index)"
                  />
                </div>
                <v-btn 
                  prepend-icon="mdi-plus"
                  variant="text"
                  @click="addCriteria"
                >
                  Add Criteria
                </v-btn>
              </div>
            </div>
          </div>
        </div>

        <div class="button-container">
          <v-btn
            color="primary"
            size="large"
            @click="submitStory"
            :loading="analyzing"
            :disabled="!story.title"
          >
            Submit Story
          </v-btn>
        </div>
      </div>

      <!-- Right Column: Help Panel -->
      <div class="analysis-panel">
        <h3 class="panel-title">Writing Tips</h3>
        <div class="invest-grid">
          <div v-for="(tip, index) in writingTips" 
               :key="index" 
               class="invest-item">
            <div class="invest-header">
              <span class="invest-letter">{{ tip.letter }}</span>
              <span class="invest-title">{{ tip.title }}</span>
            </div>
            <div class="invest-content">{{ tip.content }}</div>
          </div>
        </div>
      </div>
    </div>

    <transition name="fade">
      <div v-if="showTransition" class="animation-container">
        <video 
          ref="videoPlayer"
          class="background-video" 
          autoplay 
          loop 
          muted 
          playsinline
        >
          <source src="/videos/AdobeStock_910543395.mp4" type="video/mp4">
          <source src="/videos/AdobeStock_910543395.webm" type="video/webm">
        </video>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { v4 as uuidv4 } from 'uuid'
import AnimationTransition from '@/components/animation_transistion.vue'

const router = useRouter()
const loading = ref(false)
const error = ref(null)
const analyzing = ref(false)
const showTransition = ref(false)
const animationFrame = ref(null)
const videoPlayer = ref(null)
const isExiting = ref(false)

// Story data structure
const story = ref({
  title: '',
  text: '',
  acceptance_criteria: ['']
})

// Modified validation to only require title
const isValid = computed(() => {
  return story.value.title.trim() !== '' && 
         story.value.text.trim() !== '' && 
         story.value.acceptance_criteria.some(c => c.trim() !== '')
})

const submitStory = async () => {
  analyzing.value = true
  const storyId = uuidv4()
  
  setTimeout(() => {
    showTransition.value = true
  }, 1000)
  
  try {
    const storyData = {
      story_id: storyId,
      tenant_id: "test-tenant-001",
      title: story.value.title,
      story: story.value.text || "",
      acceptance_criteria: story.value.acceptance_criteria
        .filter(c => c.trim() !== '') || []
    }
    
    const response = await axios.post(
      `${import.meta.env.VITE_API_URL}/stories/analyze`,
      storyData
    )
    console.log('Response from analyze:', response.data)
    
    // Start the exit transition after successful API call
    isExiting.value = true
    
    // Wait for fade out before navigation
    setTimeout(async () => {
      await router.push(`/agile/${storyId}`)
    }, 1000)
    
  } catch (err) {
    console.error('Error submitting story:', err)
    if (err.response) {
      console.error('Error response:', err.response.data)
    }
    showTransition.value = false
    isExiting.value = false
    analyzing.value = false
  }
}

const writingTips = [
  {
    letter: 'U',
    title: 'User',
    content: 'Clearly identify who the user is (e.g., customer, admin, guest)'
  },
  {
    letter: 'G',
    title: 'Goal',
    content: 'State what the user wants to accomplish'
  },
  {
    letter: 'B',
    title: 'Benefit',
    content: 'Explain why this is valuable to the user'
  },
  {
    letter: 'A',
    title: 'Acceptance',
    content: 'Write clear, testable acceptance criteria'
  }
]

const addCriteria = () => {
  story.value.acceptance_criteria.push('')
}

const removeCriteria = (index) => {
  story.value.acceptance_criteria.splice(index, 1)
  if (story.value.acceptance_criteria.length === 0) {
    story.value.acceptance_criteria.push('')
  }
}

const guidelines = {
  story: {
    title: 'Story Writing Guidelines',
    items: [
      {
        icon: 'mdi-format-quote-open',
        header: 'User Story Format',
        content: [
          { prefix: 'As a', text: '[type of user]' },
          { prefix: 'I want to', text: '[perform some action]' },
          { prefix: 'So that', text: '[achieve some benefit]' }
        ]
      },
      {
        icon: 'mdi-lightbulb',
        header: 'Acceptance Criteria Tips',
        content: [
          { text: 'Use clear, specific language' },
          { text: 'One criterion per line' },
          { text: 'Include all success conditions' },
          { text: 'Consider edge cases' },
          { text: 'Make them testable' }
        ]
      }
    ]
  }
}

const STICKY_NOTES = [
  "User Stories",
  "Acceptance Criteria",
  "Technical Tasks",
  "Estimations",
  "Implementation"
];

const notes = ref([])

const isPositionValid = (x, y, existingNotes, margin) => {
  // Check if position is too close to any existing note
  for (const note of existingNotes) {
    const dx = note.x - x;
    const dy = note.y - y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    if (distance < margin) {
      return false;
    }
  }
  return true;
}

const getValidPosition = (quadrant, width, height, margin, existingNotes) => {
  const halfWidth = width / 2;
  const halfHeight = height / 2;
  let x, y, attempts = 0;
  const maxAttempts = 50; // Prevent infinite loops

  do {
    switch(quadrant) {
      case 0: // Top-left
        x = margin + Math.random() * (halfWidth - margin * 2);
        y = margin + Math.random() * (halfHeight - margin * 2);
        break;
      case 1: // Top-right
        x = halfWidth + Math.random() * (halfWidth - margin * 2);
        y = margin + Math.random() * (halfHeight - margin * 2);
        break;
      case 2: // Bottom-left
        x = margin + Math.random() * (halfWidth - margin * 2);
        y = halfHeight + Math.random() * (halfHeight - margin * 2);
        break;
      case 3: // Bottom-right
        x = halfWidth + Math.random() * (halfWidth - margin * 2);
        y = halfHeight + Math.random() * (halfHeight - margin * 2);
        break;
    }
    attempts++;
  } while (!isPositionValid(x, y, existingNotes, margin * 1.2) && attempts < maxAttempts);

  return { x, y };
}

const initializeNotes = () => {
  const margin = 160;
  const width = window.innerWidth - margin * 2;
  const height = window.innerHeight - margin * 2;
  const initialNotes = [];

  STICKY_NOTES.forEach((text, index) => {
    const quadrant = index % 4;
    const position = getValidPosition(quadrant, width, height, margin, initialNotes);
    
    // Calculate velocity based on quadrant
    let vx = 1.5 + Math.random();
    let vy = 1.5 + Math.random();
    
    // Adjust velocity direction based on quadrant
    if (quadrant === 1 || quadrant === 3) vx = -vx;
    if (quadrant === 2 || quadrant === 3) vy = -vy;

    const note = {
      id: index,
      text,
      x: position.x,
      y: position.y,
      vx,
      vy,
      rotation: Math.random() * 360,
      rotationSpeed: (Math.random() - 0.5) * 0.8
    };

    initialNotes.push(note);
  });

  notes.value = initialNotes;
}

const startAnimation = () => {
  const animate = () => {
    updateNotes();
    requestAnimationFrame(animate);
  };
  animate();
}

const updateNotes = () => {
  const margin = 160;
  const containerWidth = window.innerWidth - margin;
  const containerHeight = window.innerHeight - margin;

  notes.value.forEach((note, i) => {
    // Update position with slightly faster movement
    note.x += note.vx * 0.85;  // Increased from 0.7
    note.y += note.vy * 0.85;  // Increased from 0.7
    note.rotation += note.rotationSpeed;

    // Bounce off walls with gentler randomization
    if (note.x < margin || note.x > containerWidth - margin) {
      note.vx *= -1;
      note.vy += (Math.random() - 0.5) * 0.5;
      note.x = Math.max(margin, Math.min(note.x, containerWidth - margin));
    }
    if (note.y < margin || note.y > containerHeight - margin) {
      note.vy *= -1;
      note.vx += (Math.random() - 0.5) * 0.5;
      note.y = Math.max(margin, Math.min(note.y, containerHeight - margin));
    }

    // Collision detection with other notes
    for (let j = i + 1; j < notes.value.length; j++) {
      const other = notes.value[j];
      const dx = other.x - note.x;
      const dy = other.y - note.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      const minDistance = margin * 0.8; // Collision distance

      if (distance < minDistance) {
        // Calculate collision response
        const angle = Math.atan2(dy, dx);
        const targetX = note.x + Math.cos(angle) * minDistance;
        const targetY = note.y + Math.sin(angle) * minDistance;
        
        // Move notes apart gently
        const moveRatio = 0.1; // Gentle movement
        other.x = other.x * (1 - moveRatio) + targetX * moveRatio;
        other.y = other.y * (1 - moveRatio) + targetY * moveRatio;
        
        // Exchange velocities with dampening
        const dampening = 0.8;
        const tempVx = note.vx;
        const tempVy = note.vy;
        
        note.vx = other.vx * dampening;
        note.vy = other.vy * dampening;
        other.vx = tempVx * dampening;
        other.vy = tempVy * dampening;
        
        // Add slight rotation on collision
        const rotationImpact = 0.4;
        note.rotationSpeed += (Math.random() - 0.5) * rotationImpact;
        other.rotationSpeed += (Math.random() - 0.5) * rotationImpact;
      }
    }

    // Adjusted minimum speed
    const speed = Math.sqrt(note.vx * note.vx + note.vy * note.vy);
    if (speed < 1.2) {  // Increased from 1
      const angle = Math.random() * Math.PI * 2;
      note.vx = Math.cos(angle) * 1.8;  // Increased from 1.5
      note.vy = Math.sin(angle) * 1.8;
    }

    // Cap maximum rotation speed
    note.rotationSpeed = Math.max(-1, Math.min(1, note.rotationSpeed));
  });
}

const getNoteColor = (index) => {
  const colors = [
    { bg: '#fff7c0', shadow: '#e6d28a' }, // Yellow
    { bg: '#c0f0c0', shadow: '#8ad28a' }, // Green
    { bg: '#c0e0ff', shadow: '#8ab2d2' }, // Blue
    { bg: '#ffc0db', shadow: '#d28aa6' }, // Pink
    { bg: '#ffd7b0', shadow: '#d2a88a' }  // Orange
  ];
  const color = colors[index % colors.length];
  return {
    background: `linear-gradient(135deg, ${color.bg} 0%, ${color.shadow} 100%)`
  };
}

// Simplified back to basic video handling
const handleVideoError = (e) => {
  console.error('Video error:', e)
}

const handleVideoLoaded = () => {
  console.log('Video loaded successfully')
}

watch(showTransition, (newVal) => {
  console.log('Transition state:', newVal)
  if (newVal) {
    initializeNotes();
    startAnimation();
  } else {
    if (animationFrame.value) {
      cancelAnimationFrame(animationFrame.value);
    }
  }
})
</script>

<style scoped>
.two-column-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 2rem;
  max-width: 1800px;
  margin: 0 auto;
  min-height: 100vh;
}

.primary-content-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100%;  /* Take full height */
}

.primary-content {
  flex: 1;          /* Take remaining space */
  padding-bottom: 5rem;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(18, 18, 18, 0.8);
  position: sticky;
  bottom: 0;
  right: 0;
  z-index: 10;
  backdrop-filter: blur(10px);
}

.criteria-item {
  display: flex;
  align-items: start;
  gap: 8px;
  margin-bottom: 8px;
}

.editable-content {
  margin-bottom: 1.5rem;  /* More space between sections */
}

/* Target Vuetify input components */
:deep(.v-field) {
  border-radius: 4px !important;
  padding: 0 !important;
}

:deep(.v-text-field),
:deep(.v-textarea) {
  width: 100% !important;
  margin-bottom: 0.75rem !important;
}

.section-title,
.panel-title {
  color: #64B5F6;
  font-size: 1.25rem;
  margin-bottom: 0.75rem;
  font-weight: 500;
}

.story-section {
  margin-bottom: 1rem;
}

.story-section > * {
  margin-bottom: 1.5rem;  /* Reduced from 3rem */
}

.invest-grid {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.invest-item {
  background: rgba(48, 38, 25, 1);
  border-radius: 8px;
  padding: 1rem;
  border-left: 4px solid #FFA726;
  margin-bottom: 0.5rem;
}

.invest-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.invest-letter {
  background: #FFA726;
  color: black;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.invest-title {
  font-size: 1.2rem;
  font-weight: 500;
}

.analysis-panel {
  width: 100%;
  min-width: 0;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 1rem;
}

.writing-tips-wrapper {
  background: #121212 !important;
  height: 100%;
  overflow-y: auto;
}

.writing-tips {
  padding: 20px;
}

.tip-card {
  background: rgba(48, 38, 25, 1);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.guideline-card {
  background: rgba(48, 38, 25, 1);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.page-title {
  color: #64B5F6;
  font-size: 1.5rem;
  margin-bottom: 1rem;  /* Reduced from 1.5rem */
  font-weight: 500;
}

.input-label {
  color: #fff;
  font-size: 1rem;
  margin-bottom: 0.25rem;  /* Reduced from 0.5rem */
  font-weight: 400;
}

.form-group {
  margin-bottom: 1rem;
}

.story-form {
  background: rgba(30, 30, 30, 0.5);
  border-radius: 8px;
  padding: 1.5rem;
}

/* Adjust acceptance criteria textarea size */
.criteria-item :deep(.v-field__input) {
  min-height: 48px !important;  /* Reduced height */
  padding: 8px 12px !important;
}

.animation-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.9);
}

.background-video {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 1s ease-in-out;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.story-input {
  transition: opacity 1s ease-in-out;
  opacity: 1;
}

.story-input.fade-out {
  opacity: 0;
}
</style> 