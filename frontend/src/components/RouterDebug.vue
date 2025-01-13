<template>
  <div class="router-debug">
    <v-card>
      <v-card-title>Router Debug Info</v-card-title>
      <v-card-text>
        <pre>Current Route: {{ currentRoute }}</pre>
        <pre>Route Name: {{ routeName }}</pre>
        <pre>Route Path: {{ routePath }}</pre>
        <pre>Route Params: {{ routeParams }}</pre>
        <pre>All Routes: {{ allRoutes }}</pre>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const currentRoute = computed(() => JSON.stringify(route, null, 2))
const routeName = computed(() => route.name)
const routePath = computed(() => route.path)
const routeParams = computed(() => route.params)
const allRoutes = computed(() => JSON.stringify(router.getRoutes(), null, 2))
</script>

<style scoped>
.router-debug {
  margin-top: 20px;
  padding: 20px;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  background: #1e1e1e;
  padding: 10px;
  margin: 5px 0;
  border-radius: 4px;
}
</style> 