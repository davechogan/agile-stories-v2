<template>
  <v-app theme="dark">
    <v-app-bar>
      <v-container class="d-flex align-center">
        <v-btn 
          to="/" 
          variant="text"
          color="primary"
        >
          Story Input
        </v-btn>
        <v-btn 
          to="/agile" 
          variant="text"
          color="primary"
        >
          Analysis Results
        </v-btn>
        <v-btn 
          to="/tech" 
          variant="text"
          color="primary"
        >
          Tech Review
        </v-btn>
        <v-btn 
          to="/estimates" 
          variant="text"
          color="primary"
        >
          Estimates
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
</style>
