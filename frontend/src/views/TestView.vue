<template>
  <div class="test">
    <div class="two-column-layout">
      <!-- Left Column: Story Input -->
      <div class="primary-content-wrapper">
        <div class="primary-content">
          <h2>Story Input</h2>
          
          <div class="input-section">
            <h3>User Story</h3>
            <v-textarea
              v-model="userStory"
              auto-grow
              variant="outlined"
              placeholder="As a [user type], I want to [action], so that [benefit]"
              class="story-input"
              :rules="[v => !!v || 'Story is required']"
            ></v-textarea>
          </div>

          <div class="input-section mt-6">
            <h3>Acceptance Criteria</h3>
            <v-textarea
              v-model="acceptanceCriteria"
              auto-grow
              variant="outlined"
              placeholder="Enter each acceptance criterion on a new line"
              class="ac-input"
              :rules="[v => !!v || 'At least one acceptance criterion is required']"
            ></v-textarea>
          </div>

          <div class="input-section mt-6">
            <h3>Context</h3>
            <div class="input-hint">Provide any background information or business context that helps understand this story</div>
            <v-textarea
              v-model="context"
              auto-grow
              variant="outlined"
              placeholder="Example: This story is part of the new notification system. Currently, users have no way to see broadcast messages..."
              class="context-input"
              rows="3"
            ></v-textarea>
          </div>
        </div>

        <!-- Sticky Footer -->
        <div class="sticky-footer">
          <div class="footer-content">
            <div class="footer-buttons">
              <v-btn 
                color="primary" 
                size="large"
                prepend-icon="mdi-magic-staff"
                :loading="loading"
                :disabled="!isValid"
                @click="submitStory"
              >
                Improve Story
              </v-btn>
            </div>
            <div class="footer-hint" v-if="!isValid">
              Please enter both a user story and acceptance criteria
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Guidelines -->
      <div class="guidelines-panel">
        <div class="guidelines-section">
          <h3>Story Writing Guidelines</h3>
          <div class="guideline-card">
            <div class="guideline-header">
              <v-icon color="primary" class="mr-2">mdi-format-quote-open</v-icon>
              User Story Format
            </div>
            <div class="guideline-content">
              <p><strong>As a</strong> [type of user]</p>
              <p><strong>I want to</strong> [perform some action]</p>
              <p><strong>So that</strong> [achieve some benefit]</p>
            </div>
          </div>

          <div class="guideline-card mt-4">
            <div class="guideline-header">
              <v-icon color="success" class="mr-2">mdi-checkbox-marked-circle</v-icon>
              INVEST Principles
            </div>
            <div class="guideline-content">
              <ul class="invest-list">
                <li><strong>Independent:</strong> Minimal dependencies on other stories</li>
                <li><strong>Negotiable:</strong> Flexible in implementation details</li>
                <li><strong>Valuable:</strong> Delivers clear value to users</li>
                <li><strong>Estimable:</strong> Can be sized relatively easily</li>
                <li><strong>Small:</strong> Completable within one sprint</li>
                <li><strong>Testable:</strong> Clear criteria for completion</li>
              </ul>
            </div>
          </div>

          <div class="guideline-card mt-4">
            <div class="guideline-header">
              <v-icon color="warning" class="mr-2">mdi-lightbulb</v-icon>
              Acceptance Criteria Tips
            </div>
            <div class="guideline-content">
              <ul>
                <li>Use clear, specific language</li>
                <li>One criterion per line</li>
                <li>Include all success conditions</li>
                <li>Consider edge cases</li>
                <li>Make them testable</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const context = ref('')
const userStory = ref('')
const acceptanceCriteria = ref('')
const loading = ref(false)

const isValid = computed(() => {
  return userStory.value.trim() && acceptanceCriteria.value.trim()
})

const submitStory = async () => {
  if (!isValid.value) return
  
  loading.value = true
  try {
    // Your existing submission logic
    // Now includes context: context.value
  } finally {
    loading.value = false
  }
}
</script>

<style>
.two-column-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 2rem;
  max-width: 1800px;
  margin: 0 auto;
  min-height: 100vh;
  position: relative;
}

.primary-content-wrapper {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.primary-content {
  position: sticky;
  top: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
  max-height: calc(100vh - 8rem);
  overflow-y: auto;
  flex-grow: 1;
}

.input-section {
  margin-top: 2.5rem;
}

.input-section:first-child {
  margin-top: 1.5rem;
}

.story-input,
.ac-input {
  margin-top: 1rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}

/* Guidelines Panel */
.guidelines-panel {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
}

.guideline-card {
  background: rgba(33, 150, 243, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.guideline-header {
  background: rgba(33, 150, 243, 0.2);
  padding: 1rem;
  font-weight: 500;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
}

.guideline-content {
  padding: 1rem;
  line-height: 1.6;
}

.invest-list li {
  margin-bottom: 0.5rem;
}

/* Sticky Footer */
.sticky-footer {
  position: fixed;
  bottom: 0;
  width: calc(50% - 2rem);
  background: linear-gradient(
    to top,
    rgba(30, 30, 30, 1) 0%,
    rgba(30, 30, 30, 0.9) 70%,
    rgba(30, 30, 30, 0) 100%
  );
  padding: 1rem 0;
  margin-top: -4rem;
  pointer-events: none;
  z-index: 10;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  pointer-events: auto;
  padding: 0 2rem;
}

.footer-hint {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  font-style: italic;
}

/* Style the textarea */
:deep(.v-field__input) {
  color: rgba(255, 255, 255, 0.87) !important;
  font-family: inherit !important;
  line-height: 1.6 !important;
}

:deep(.v-field) {
  border-color: rgba(255, 255, 255, 0.1) !important;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .two-column-layout {
    grid-template-columns: 1fr;
  }
  
  .primary-content {
    position: relative;
    top: 0;
    max-height: none;
  }
  
  .sticky-footer {
    position: fixed;
    width: 100%;
    left: 0;
    right: 0;
    margin-top: 0;
  }
  
  .guidelines-panel {
    margin-top: 2rem;
  }
}

.input-hint {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 0.5rem;
  font-style: italic;
}

.context-input {
  margin-top: 0.5rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}

.context-input :deep(.v-field__input) {
  min-height: 80px !important;
}
</style> 