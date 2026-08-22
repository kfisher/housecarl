<script setup>
import { onMounted, ref } from 'vue'

import RandomTaskCountModal from '@/components/RandomTaskCountModal.vue'
import { taskStateLabels } from '@/constants/taskState'

const randomTasks = ref([])
const loading = ref(false)
const error = ref(null)

const lastCount = ref(4)
const countModalOpen = ref(false)

const selectedTaskId = ref(null)

const stateLabels = taskStateLabels

const stateTagClass = {
  0: 'is-light',
  1: 'is-danger',
  2: 'is-warning',
  3: 'is-success',
}

async function fetchRandomTasks() {
  loading.value = true
  error.value = null
  try {
    const response = await fetch('/api/random-tasks')
    if (!response.ok) throw new Error('Failed to load random tasks')
    randomTasks.value = await response.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchRandomTasks)

async function generate(count) {
  error.value = null
  try {
    const response = await fetch('/api/random-tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ count }),
    })
    if (!response.ok) throw new Error('Failed to generate random tasks')
    randomTasks.value = await response.json()
    lastCount.value = count
    selectedTaskId.value = null
  } catch (err) {
    error.value = err.message
  }
}

function openCountModal() {
  countModalOpen.value = true
}

function closeCountModal() {
  countModalOpen.value = false
}

async function confirmCount(count) {
  closeCountModal()
  await generate(count)
}

function selectRandomTask() {
  if (randomTasks.value.length === 0) return
  const index = Math.floor(Math.random() * randomTasks.value.length)
  selectedTaskId.value = randomTasks.value[index].id
}
</script>

<template>
  <div class="random-view">
    <div class="random-view__header">
      <h1 class="title">Random</h1>

      <div class="random-view__header-actions">
        <button class="button" type="button" title="Select Random Task" @click="selectRandomTask">
          <span class="icon is-small">
            <font-awesome-icon :icon="['fas', 'dice-d20']" size="sm" />
          </span>
          <span>Select Task</span>
        </button>

        <button class="button" type="button" @click="openCountModal">
          <span class="icon is-small">
            <font-awesome-icon :icon="['fas', 'arrows-rotate']" size="sm" />
          </span>
          <span>Generate</span>
        </button>
      </div>
    </div>

    <p v-if="error" class="notification is-danger">{{ error }}</p>

    <table v-else class="table is-fullwidth is-hoverable random-view__table">
      <tbody>
        <tr
          v-for="entry in randomTasks"
          :key="entry.id"
          class="random-view__task-row"
          :class="{ 'is-dark': entry.id === selectedTaskId }"
        >
          <td class="random-view__cell-middle random-view__number">{{ entry.number }}</td>
          <td class="random-view__cell-middle random-view__actions">
            <span class="random-view__row-actions">
              <button class="button is-small is-text" type="button" title="Today">
                <font-awesome-icon :icon="['fas', 'calendar-day']" size="sm" />
              </button>
              <button class="button is-small is-text" type="button" title="Complete">
                <font-awesome-icon :icon="['fas', 'check']" size="sm" />
              </button>
            </span>
          </td>
          <td class="random-view__cell-middle">
            <span class="tag random-view__state-tag" :class="stateTagClass[entry.task.state]">
              {{ stateLabels[entry.task.state] }}
            </span>
          </td>
          <td class="random-view__cell-middle random-view__room">{{ entry.task.room.title }}</td>
          <td class="random-view__task-column">
            <p>{{ entry.task.title }}</p>
            <p v-if="entry.task.description" class="random-view__task-description">
              {{ entry.task.description }}
            </p>
          </td>
        </tr>
        <tr v-if="!loading && randomTasks.length === 0">
          <td colspan="5" class="has-text-centered has-text-grey">
            No random tasks yet. Click Generate to get started.
          </td>
        </tr>
      </tbody>
    </table>

    <RandomTaskCountModal
      :open="countModalOpen"
      :count="lastCount"
      @confirm="confirmCount"
      @close="closeCountModal"
    />
  </div>
</template>

<style scoped>
.random-view {
  padding: 1rem 1.5rem 2rem;
}

.random-view__header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.random-view__header .title {
  margin-bottom: 0;
}

.random-view__header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.random-view__row-actions {
  display: flex;
  gap: 0.25rem;
}

.random-view__cell-middle {
  vertical-align: middle;
}

.random-view__number {
  width: 1%;
  white-space: nowrap;
  font-weight: 600;
  color: var(--bulma-text-weak);
}

.random-view__actions {
  white-space: nowrap;
}

.random-view__room {
  width: 1%;
  white-space: nowrap;
}

.random-view__task-column {
  width: 100%;
}

.random-view__task-description {
  font-size: 0.85em;
  font-style: italic;
  color: var(--bulma-text-weak);
}

.random-view__state-tag {
  width: 5.5rem;
}
</style>
