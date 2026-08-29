<!--
Copyright 2026 Kevin Fisher. All rights reserved.
SPDX-License-Identifier: AGPL-3.0-only
-->

<script setup>
import NavSidebar from '@/components/NavSidebar.vue'
import { theme, toggleTheme } from '@/theme'
</script>

<template>
  <div class="app-shell">
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <span class="navbar-item app-navbar__brand">Housecarl</span>
      </div>
      <div class="navbar-menu is-active">
        <div class="navbar-end">
          <div class="navbar-item">
            <button
              type="button"
              class="button is-text"
              aria-label="Toggle theme"
              title="Toggle theme"
              @click="toggleTheme"
            >
              <font-awesome-icon :icon="['fas', theme === 'dark' ? 'moon' : 'sun']" />
            </button>
          </div>
        </div>
      </div>
    </nav>

    <div class="columns is-gapless app-layout">
      <div class="column is-2 app-layout__nav">
        <NavSidebar />
      </div>
      <div class="column app-layout__content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-shell {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-shell .navbar {
  background-color: var(--bulma-scheme-main);
  border-bottom: 1px solid var(--bulma-border-weak);
}

.app-navbar__brand {
  font-weight: 700;
  font-size: 1.25rem;
}

.app-layout {
  flex: 1;
  margin: 0;
}

.app-layout__nav {
  flex: none;
  width: 16rem;
  background-color: var(--bulma-scheme-main-bis);
  border-right: 1px solid var(--bulma-border-weak);
  padding: 1.5rem 1rem;
}

.app-layout__content {
  padding: 1.5rem;
}
</style>
