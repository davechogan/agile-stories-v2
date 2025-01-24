<template>
  <div class="editable-section" :class="{ 'is-editing': isEditing }">
    <div class="section-header">
      <h3 class="section-title">{{ title }}</h3>
      <v-btn 
        v-if="!isEditing"
        icon="mdi-pencil"
        size="small"
        variant="text"
        class="edit-button"
        @click="startEditing"
      ></v-btn>
    </div>
    
    <div class="content-wrapper">
      <!-- View Mode -->
      <div v-if="!isEditing" class="content">
        <slot v-if="type === 'list' && Array.isArray(modelValue)">
          <div v-for="(item, index) in modelValue" 
               :key="index"
               class="list-item">
            <span class="bullet">•</span>
            {{ item }}
          </div>
        </slot>
        <slot v-else>
          {{ modelValue }}
        </slot>
      </div>
      
      <!-- Edit Mode -->
      <template v-else>
        <v-textarea
          v-if="type === 'text' || type === 'list'"
          v-model="editedContent"
          :placeholder="placeholder"
          auto-grow
          variant="outlined"
          class="edit-field"
          @keyup.esc="cancelEdit"
        ></v-textarea>
        <v-text-field
          v-else
          v-model="editedContent"
          :placeholder="placeholder"
          variant="outlined"
          class="edit-field"
          @keyup.esc="cancelEdit"
          @keyup.enter="saveEdit"
        ></v-text-field>
        
        <div class="edit-actions">
          <v-btn 
            size="small"
            color="success"
            class="mr-2"
            @click="saveEdit"
          >Save</v-btn>
          <v-btn 
            size="small"
            color="error"
            @click="cancelEdit"
          >Cancel</v-btn>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Array],
    required: true
  },
  title: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'text',
    validator: (value) => ['text', 'list', 'single-line'].includes(value)
  },
  placeholder: {
    type: String,
    default: 'Enter content...'
  }
})

const emit = defineEmits(['update:modelValue'])

const isEditing = ref(false)
const editedContent = ref('')

const startEditing = () => {
  editedContent.value = props.type === 'list' 
    ? props.modelValue.join('\n')
    : props.modelValue
  isEditing.value = true
}

const saveEdit = () => {
  const newValue = props.type === 'list'
    ? editedContent.value.split('\n').filter(line => line.trim())
    : editedContent.value.trim()
  
  emit('update:modelValue', newValue)
  isEditing.value = false
}

const cancelEdit = () => {
  isEditing.value = false
}
</script>

<style scoped>
.editable-section {
  position: relative;
  padding: 1.5rem;
  background: #333;
  border-radius: 8px;
  margin-bottom: 1rem;
  transition: background-color 0.2s;
}

.editable-section:hover {
  background: #383838;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-title {
  color: #fff;
  font-size: 1.1rem;
  font-weight: normal;
  margin: 0;
}

.edit-button {
  opacity: 0;
  transition: opacity 0.2s;
}

.editable-section:hover .edit-button {
  opacity: 1;
}

.content {
  line-height: 1.6;
  white-space: pre-wrap;
  color: rgba(255, 255, 255, 0.9);
}

.list-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.bullet {
  margin-right: 0.5rem;
  color: #64B5F6;
}

.edit-field {
  background: #333;
  border-radius: 4px;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.75rem;
  gap: 0.5rem;
}

.is-editing {
  background: #383838;
}
</style> 