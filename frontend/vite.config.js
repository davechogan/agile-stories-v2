import { fileURLToPath, URL } from 'node:url'


import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/


import { defineConfig } from 'vite'
import Vue from '@vitejs/plugin-vue'
import { liveDesigner } from '@pinegrow/vite-plugin'

export default defineConfig({
  plugins: [
    liveDesigner({
      //... 
    }),
    Vue(),
    //...
  ],
  //...
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})

