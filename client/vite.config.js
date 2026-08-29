import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        // Bulma's own source triggers Sass deprecation warnings (e.g. the
        // legacy if() syntax); quietDeps silences warnings that originate
        // in dependencies while still surfacing them for our own styles.
        quietDeps: true,
      },
    },
  },
})
