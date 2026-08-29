<!--
Copyright 2026 Kevin Fisher. All rights reserved.
SPDX-License-Identifier: AGPL-3.0-only
-->

<script setup>
import { nextTick, ref, watch } from 'vue'

import { taskStateOptions } from '@/constants/taskState'

const props = defineProps({
  open: {
    type: Boolean,
    default: false,
  },
  taskTitle: {
    type: String,
    default: '',
  },
  roomTitle: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['confirm', 'close'])

const goodState = taskStateOptions.find((option) => option.label === 'Good').value

function todayDateString() {
  const now = new Date()
  const localMidnight = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
  return localMidnight.toISOString().slice(0, 10)
}

const state = ref(goodState)
const performedDate = ref(todayDateString())
const dateInputRef = ref(null)

watch(
  () => props.open,
  async (isOpen) => {
    if (!isOpen) return
    state.value = goodState
    performedDate.value = todayDateString()
    await nextTick()
    dateInputRef.value?.focus()
  },
)

function confirm() {
  emit('confirm', {
    state: state.value,
    last_performed: performedDate.value,
  })
}
</script>

<template>
  <div class="modal" :class="{ 'is-active': open }">
    <div class="modal-background" @click="emit('close')"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Complete Task</p>
        <button class="delete" aria-label="close" type="button" @click="emit('close')"></button>
      </header>
      <section class="modal-card-body">
        <div class="field">
          <p class="complete-task-modal__task-title">{{ taskTitle }}</p>
          <p class="complete-task-modal__room-title">{{ roomTitle }}</p>
        </div>

        <div class="field">
          <label class="label">State</label>
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model.number="state">
                <option
                  v-for="option in taskStateOptions"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </div>
          </div>
        </div>

        <div class="field">
          <label class="label">Performed</label>
          <div class="control">
            <input ref="dateInputRef" v-model="performedDate" class="input" type="date" />
          </div>
        </div>
      </section>
      <footer class="modal-card-foot complete-task-modal__foot">
        <div class="buttons">
          <button class="button is-primary" type="button" @click="confirm">Save</button>
          <button class="button" type="button" @click="emit('close')">Cancel</button>
        </div>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.modal-card-head {
  box-shadow: none;
}

.modal-card-foot {
  background-color: var(--bulma-scheme-main);
}

.complete-task-modal__foot {
  justify-content: flex-end;
}

.complete-task-modal__task-title {
  font-weight: 600;
}

.complete-task-modal__room-title {
  font-size: 0.85em;
  color: var(--bulma-text-weak);
}
</style>
