<template>
  <v-dialog
    v-model="show"
    fullscreen
    transition="dialog-bottom-transition"
  >
    <v-card class="editor-card">
      <v-toolbar dark color="rgb(30, 41, 59)">
        <v-btn icon @click="cancel">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>{{ title }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn text @click="save">
          Save
        </v-btn>
      </v-toolbar>

      <v-card-text class="editor-content">
        <v-textarea
          v-if="type === 'text' || type === 'list'"
          v-model="editedContent"
          :placeholder="placeholder"
          auto-grow
          variant="outlined"
          class="mt-4 editor-textarea"
          :rows="15"
          :height="400"
          bg-color="rgb(18, 24, 36)"
        ></v-textarea>
        <v-text-field
          v-else
          v-model="editedContent"
          :placeholder="placeholder"
          variant="outlined"
          class="mt-4"
          height="56"
          bg-color="rgb(18, 24, 36)"
        ></v-text-field>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.editor-card {
  background-color: rgb(18, 24, 36) !important;
}

.editor-content {
  height: calc(100vh - 64px);
  padding: 16px;
  background-color: rgb(18, 24, 36);
}

:deep(.v-field) {
  background-color: rgb(18, 24, 36) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
}

:deep(.v-field__input) {
  color: rgba(255, 255, 255, 0.87) !important;
  font-size: 16px !important;
  line-height: 1.6 !important;
  font-family: inherit !important;
}

:deep(.editor-textarea textarea) {
  font-family: inherit !important;
  line-height: 1.6 !important;
  padding: 12px !important;
  min-height: 300px !important;
}

:deep(.v-toolbar) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
</style>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  modelValue: string | string[]
  show: boolean
  title: string
  type: 'single-line' | 'text' | 'list'
  placeholder?: string
}>()

const emit = defineEmits<{
  (e: 'update:show', value: boolean): void
  (e: 'save', value: string): void
  (e: 'cancel'): void
}>()

const editedContent = ref('')

// Initialize content when dialog opens AND when modelValue changes
watch([() => props.show, () => props.modelValue], ([newShow, newValue]) => {
  if (newShow || newValue !== undefined) {
    editedContent.value = props.type === 'list' 
      ? (props.modelValue as string[]).join('\n')
      : props.modelValue as string
    console.log('Updated editor content:', editedContent.value)
  }
}, { immediate: true })

const save = () => {
  emit('save', editedContent.value)
  emit('update:show', false)
}

const cancel = () => {
  emit('cancel')
  emit('update:show', false)
}
</script> 