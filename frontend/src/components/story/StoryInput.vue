<template>
  <div class="story-input">
    <v-card>
      <v-card-title>Create User Story</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submitStory">
          <v-textarea
            v-model="story"
            label="User Story"
            placeholder="As a [user], I want to [action] so that [benefit]"
            :rules="[v => !!v || 'Story is required']"
          />
          
          <v-expansion-panels>
            <v-expansion-panel title="Acceptance Criteria">
              <v-expansion-panel-text>
                <div v-for="(criterion, index) in acceptanceCriteria" :key="index" class="d-flex align-center mb-2">
                  <v-text-field
                    v-model="acceptanceCriteria[index]"
                    label="Criterion"
                    hide-details
                  />
                  <v-btn icon class="ml-2" @click="removeCriterion(index)">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </div>
                <v-btn
                  prepend-icon="mdi-plus"
                  variant="text"
                  @click="addCriterion"
                >
                  Add Criterion
                </v-btn>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>

          <v-btn
            type="submit"
            color="primary"
            class="mt-4"
            :loading="isSubmitting"
          >
            Analyze Story
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useMutation } from '@vue/apollo-composable'
import { ANALYZE_STORY } from '@/graphql/mutations/analyzeStory'

const story = ref('')
const acceptanceCriteria = ref([''])
const isSubmitting = ref(false)

// Define the mutation
const { mutate: analyzeStory, loading, error, onDone } = useMutation(ANALYZE_STORY)

const addCriterion = () => {
  acceptanceCriteria.value.push('')
}

const removeCriterion = (index: number) => {
  acceptanceCriteria.value.splice(index, 1)
}

// Handle successful analysis
onDone((result) => {
  console.log('Analysis complete:', result.data.analyzeStory)
  // TODO: Emit event to parent component to show results
  emit('analysis-complete', result.data.analyzeStory)
})

const submitStory = async () => {
  isSubmitting.value = true
  try {
    await analyzeStory({
      input: {
        story: story.value,
        acceptanceCriteria: acceptanceCriteria.value.filter(Boolean)
      }
    })
  } catch (err) {
    console.error('Error:', err)
  } finally {
    isSubmitting.value = false
  }
}

// Define emits
const emit = defineEmits<{
  (e: 'analysis-complete', analysis: any): void
}>()
</script>

<style scoped lang="scss">
.story-input {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}
</style> 