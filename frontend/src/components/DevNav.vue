<template>
  <v-app-bar>
    <v-container class="d-flex align-center">
      <router-link 
        v-for="route in routes" 
        :key="route.path"
        :to="route.path"
        class="mr-4"
      >
        <v-btn 
          variant="text"
          :color="$route.path === route.path ? 'primary' : undefined"
        >
          {{ route.label }}
        </v-btn>
      </router-link>
    </v-container>
  </v-app-bar>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const $route = useRoute()

const routes = [
  { path: '/', label: 'Story Input' },
  { path: '/story', label: 'Test Format' },
  { path: '/agile', label: 'Agile Review' },
  { path: '/tech', label: 'Tech Review' },
  { path: '/techreview', label: 'Old Tech Review' },
  { path: '/estimate', label: 'Estimation' }
]
</script>

<style scoped>
.dev-nav {
  background: rgba(255, 152, 0, 0.1);
  border-bottom: 2px solid rgba(255, 152, 0, 0.2);
  padding: 0.5rem;
}

.dev-nav-content {
  max-width: 1800px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  padding: 0 2rem;
}

.dev-label {
  color: #FF9800;
  font-weight: 500;
  margin-right: 1rem;
}
</style> 