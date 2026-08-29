// Copyright 2026 Kevin Fisher. All rights reserved.
// SPDX-License-Identifier: AGPL-3.0-only
import { ref } from 'vue'

const STORAGE_KEY = 'housecarl-theme'

/**
 * Applies the current value of `theme`.
 */
function applyTheme() {
  document.documentElement.setAttribute('data-theme', theme.value);
}

/**
 * Gets the preferred theme (dark vs light) based on system preferences.
 */
function getPreferredTheme() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
};

/**
 * Returns the theme saved to local storage.
 *
 * If local storage is unavailable or the theme has not been saved, returns the
 * preferred theme based on system preferences.
 */
function getStoredTheme() {
  try {
    switch (localStorage.getItem(STORAGE_KEY)) {
      case 'dark':
        return 'dark';
      case 'light':
        return 'light';
      default:
        return getPreferredTheme();
    }
  } catch {
    return getPreferredTheme();
  }
}

/**
 * Sets the theme to `name`.
 */
function setTheme(name) {
  theme.value = name;
  applyTheme();
  try {
    localStorage.setItem(STORAGE_KEY, name)
  } catch {
    // localStorage unavailable; theme just won't persist across reloads.
  }
}

/**
 * The current theme ('dark' or 'light').
 */
export const theme = ref(getStoredTheme())

/**
 * Toggles the theme between light and dark modes.
 *
 * When toggled, the theme will be saved to local storage so that it persists.
 */
export function toggleTheme() {
  setTheme(theme.value === 'dark' ? 'light' : 'dark')
}

applyTheme();

