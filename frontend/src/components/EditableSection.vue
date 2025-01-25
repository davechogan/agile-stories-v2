<template>
  <div class="editable-content">
    <template v-if="!isEditing">
      <div class="content-display">
        <h3 class="section-heading">{{ title }}</h3>
        <div v-if="type === 'single-line'" class="content-text">{{ modelValue }}</div>
        <pre v-else-if="type === 'text'" class="content-text">{{ modelValue }}</pre>
        <ul v-else-if="type === 'list'" class="content-list">
          <li v-for="(item, index) in modelValue" :key="index">{{ item }}</li>
        </ul>
      </div>
      <v-btn 
        size="small" 
        color="primary" 
        class="edit-btn"
        icon="mdi-pencil"
        @click="startEditing"
      ></v-btn>
    </template>
    
    <template v-else>
      <h3 class="section-heading">{{ title }}</h3>
      <v-textarea
        v-if="type === 'text' || type === 'list'"
        v-model="editedContent"
        auto-grow
        variant="outlined"
        :placeholder="placeholder"
        class="edit-textarea"
      ></v-textarea>
      <v-text-field
        v-else
        v-model="editedContent"
        variant="outlined"
        :placeholder="placeholder"
        class="edit-input"
      ></v-text-field>
      <div class="edit-actions">
        <v-btn 
          size="small" 
          color="success" 
          @click="saveContent"
          class="mr-2"
        >Save</v-btn>
        <v-btn 
          size="small" 
          color="error" 
          @click="cancelEdit"
        >Cancel</v-btn>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  modelValue: string | string[]
  title: string
  type: 'single-line' | 'text' | 'list'
  placeholder?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | string[]): void
}>()

const isEditing = ref(false)
const editedContent = ref('')

const startEditing = () => {
  editedContent.value = props.type === 'list' 
    ? (props.modelValue as string[]).join('\n')
    : props.modelValue as string
  isEditing.value = true
}

const saveContent = () => {
  if (props.type === 'list') {
    const newList = editedContent.value
      .split('\n')
      .map(item => item.trim())
      .filter(item => item.length > 0)
    emit('update:modelValue', newList)
  } else {
    emit('update:modelValue', editedContent.value)
  }
  isEditing.value = false
}

const cancelEdit = () => {
  isEditing.value = false
}
</script>

<style scoped>
.editable-content {
  position: relative;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1rem 0;
  transition: all 0.3s ease;
}

.edit-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.editable-content:hover .edit-btn {
  opacity: 1;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
}

.edit-textarea {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.section-heading {
  font-size: 1.25rem;
  font-weight: normal;
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.87);
}

.content-text {
  white-space: pre-wrap;
  line-height: 1.6;
}

.content-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.content-list li {
  display: flex;
  align-items: baseline;
  margin-bottom: 0.5rem;
}

.content-list li::before {
  content: "•";
  color: #64B5F6;
  margin-right: 0.5rem;
}

:deep(.v-field__input) {
  color: rgba(255, 255, 255, 0.87) !important;
  font-family: inherit !important;
  line-height: 1.6 !important;
}

:deep(.v-field) {
  border-color: rgba(255, 255, 255, 0.1) !important;
}
</style> 