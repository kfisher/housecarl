<!--
Copyright 2026 Kevin Fisher. All rights reserved.
SPDX-License-Identifier: AGPL-3.0-only
-->

<script setup>
import { ref, watch } from 'vue'

const counts = [4, 6, 12, 20]

const props = defineProps({
  open: {
    type: Boolean,
    default: false,
  },
  count: {
    type: Number,
    default: 4,
  },
})

const emit = defineEmits(['confirm', 'close'])

const selectedCount = ref(props.count)

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) selectedCount.value = props.count
  },
)

function confirm() {
  emit('confirm', selectedCount.value)
}
</script>

<template>
  <div class="modal" :class="{ 'is-active': open }">
    <div class="modal-background" @click="emit('close')"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Generate Random Tasks</p>
        <button class="delete" aria-label="close" type="button" @click="emit('close')"></button>
      </header>
      <section class="modal-card-body">
        <div class="field">
          <label class="label">Number of Tasks</label>
          <div class="control">
            <div class="buttons has-addons">
              <button
                v-for="option in counts"
                :key="option"
                class="button"
                :class="{ 'is-link': option === selectedCount }"
                type="button"
                @click="selectedCount = option"
              >
                {{ option }}
              </button>
            </div>
          </div>
        </div>
      </section>
      <footer class="modal-card-foot random-task-count-modal__foot">
        <div class="buttons">
          <button class="button is-primary" type="button" @click="confirm">Generate</button>
          <button class="button" type="button" @click="emit('close')">Cancel</button>
        </div>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.random-task-count-modal__foot {
  justify-content: flex-end;
}
</style>
