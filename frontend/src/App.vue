<template>
  <v-app theme="dark">
    <v-app-bar>
      <v-container class="d-flex align-center">
        <router-link 
          to="/" 
          class="nav-link"
        >
          Agile Advisor
        </router-link>
        
        <v-spacer></v-spacer>

        <v-btn
          icon="mdi-cog"
          variant="text"
          class="settings-button"
          to="/settings"
        >
          <v-icon>mdi-cog</v-icon>
        </v-btn>
      </v-container>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script setup>
// No additional setup needed
</script>

<style>
:root {
  --v-theme-surface: #1E1E1E;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  background-color: #121212;
}

.v-application {
  background-color: #121212 !important;
}

.v-main {
  background-color: #121212;
  padding-top: 24px !important;
}

.v-textarea .v-field__input {
  min-height: unset !important;
}

.v-btn {
  text-transform: none;
}

/* Check these global styles */
.v-application {
  /* Are there any width/height constraints? */
}

.v-main {
  /* Check main content container settings */
}

/* Add responsive container width */
.v-container {
  max-width: 100% !important;
  width: 100%;
}

.nav-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  padding: 0 1rem;
  font-size: 1.3rem;
  font-weight: 500;
}

.settings-btn {
  opacity: 0.7;
}

@media (max-width: 960px) {
  .hide-mobile {
    display: none !important;
  }
}
</style>
