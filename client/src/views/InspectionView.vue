<!--
Copyright 2026 Kevin Fisher. All rights reserved.
SPDX-License-Identifier: AGPL-3.0-only
-->

<script setup>
import { computed, onMounted, ref, watch } from 'vue'

import { createTaskNote, fetchTaskNotes } from '@/api/taskNotes'
import { taskStateOptions } from '@/constants/taskState'

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
})

const room = ref(null)
const loading = ref(false)
const error = ref(null)

const stateOptions = taskStateOptions
const stateButtonClass = {
  1: 'is-danger',
  2: 'is-warning',
  3: 'is-success',
}

const steps = ref([])
const currentIndex = ref(0)

const currentStep = computed(() => steps.value[currentIndex.value] ?? null)
const isComplete = computed(
  () => steps.value.length > 0 && currentIndex.value >= steps.value.length,
)

async function fetchRoom() {
  loading.value = true
  error.value = null
  try {
    const response = await fetch(`/api/rooms/${props.id}`)
    if (!response.ok) throw new Error('Failed to load room')
    room.value = await response.json()
    steps.value = room.value.tasks.map((task) => ({
      task,
      selectedState: task.state,
      noteText: '',
      notes: [],
      notesLoaded: false,
    }))
    currentIndex.value = 0
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchRoom)

async function loadNotesForCurrentStep() {
  const step = currentStep.value
  if (!step || step.notesLoaded) return
  step.notes = await fetchTaskNotes(step.task.id)
  step.notesLoaded = true
}

watch(currentStep, loadNotesForCurrentStep, { immediate: true })

const MONTH_NAMES = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
]

function formatDate(value) {
  const date = new Date(value)
  const day = String(date.getDate()).padStart(2, '0')
  const month = MONTH_NAMES[date.getMonth()]
  return `${day} ${month} ${date.getFullYear()}`
}

function goBack() {
  currentIndex.value = Math.max(0, currentIndex.value - 1)
}

async function goNext() {
  const step = currentStep.value
  if (step) {
    const updates = { last_inspected: new Date().toISOString() }
    if (step.selectedState !== step.task.state) {
      updates.state = step.selectedState
    }

    const requests = [
      fetch(`/api/tasks/${step.task.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates),
      }),
    ]

    const noteText = step.noteText.trim()
    if (noteText) {
      requests.push(createTaskNote(step.task.id, noteText))
    }

    const [taskResponse, note] = await Promise.all(requests)
    if (!taskResponse.ok) return

    step.task.state = step.selectedState
    step.task.last_inspected = updates.last_inspected
    if (note) {
      step.notes = [note, ...step.notes]
      step.noteText = ''
    }
  }

  currentIndex.value += 1
}
</script>

<template>
  <div class="inspection-view">
    <template v-if="!loading && !error">
      <div v-if="currentStep" class="inspection-view__task">
        <h1 class="title">{{ currentStep.task.title }}</h1>
        <p v-if="currentStep.task.description" class="inspection-view__description">
          {{ currentStep.task.description }}
        </p>

        <div class="inspection-view__meta">
          <p>
            <strong>Last Inspected</strong><br />
            {{ formatDate(currentStep.task.last_inspected) }}
          </p>
          <p class="ml-5">
            <strong>Last Performed</strong><br />
            {{ formatDate(currentStep.task.last_performed) }}
          </p>
        </div>

        <div class="field">
          <label class="label">State</label>
          <div class="control">
            <div class="buttons has-addons">
              <button
                v-for="option in stateOptions"
                :key="option.value"
                type="button"
                class="button is-flex-grow-1"
                :class="{ [stateButtonClass[option.value]]: currentStep.selectedState === option.value }"
                @click="currentStep.selectedState = option.value"
              >
                {{ option.label }}
              </button>
            </div>
          </div>
        </div>

        <div class="field">
          <label class="label">Notes</label>
          <div class="control">
            <textarea
              v-model="currentStep.noteText"
              class="textarea"
              rows="3"
              placeholder="Add a note"
            ></textarea>
          </div>
        </div>

        <div class="inspection-view__notes-list">
          <p v-if="!currentStep.notesLoaded" class="has-text-grey">Loading notes…</p>
          <p v-else-if="currentStep.notes.length === 0" class="has-text-grey">No notes yet.</p>
          <div v-for="note in currentStep.notes" :key="note.id" class="inspection-view__note">
            <p class="inspection-view__note-date">{{ formatDate(note.date) }}</p>
            <p>{{ note.text }}</p>
          </div>
        </div>

        <div class="buttons inspection-view__nav">
          <button
            class="button"
            type="button"
            :disabled="currentIndex === 0"
            @click="goBack"
          >
            Back
          </button>
          <button class="button is-primary" type="button" @click="goNext">Next</button>
        </div>
      </div>

      <div v-else-if="isComplete || steps.length === 0" class="inspection-view__complete">
        <h1 class="title">Inspection Complete</h1>
        <router-link :to="{ name: 'room', params: { id: props.id } }" class="button is-primary">
          Return to Room
        </router-link>
      </div>
    </template>
  </div>
</template>

<style scoped>
.inspection-view {
  padding: 1rem 1.5rem 2rem;
  max-width: 40rem;
  margin: 0 auto;
}

.inspection-view__description {
  color: var(--bulma-text-weak);
  margin-bottom: 1rem;
}

.inspection-view__meta {
  margin-bottom: 1.5rem;
  font-size: 0.9em;
  display: flex;
}

.inspection-view__notes-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.inspection-view__note {
  border-top: 1px solid var(--bulma-border);
  padding-top: 0.5rem;
}

.inspection-view__note-date {
  font-size: 0.8em;
  color: var(--bulma-text-weak);
}

.inspection-view__nav {
  justify-content: space-between;
}

.inspection-view__complete {
  text-align: center;
  margin-top: 3rem;
}
</style>
