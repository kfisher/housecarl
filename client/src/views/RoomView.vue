<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

import CompleteTaskModal from '@/components/CompleteTaskModal.vue'
import ConfirmModal from '@/components/ConfirmModal.vue'
import TaskFormModal from '@/components/TaskFormModal.vue'
import { taskStateLabels, taskStateOptions } from '@/constants/taskState'
import { useRoomsStore } from '@/stores/rooms'

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
})

const roomsStore = useRoomsStore()

const room = ref(null)
const loading = ref(false)
const error = ref(null)

const searchText = ref('')
const groupBy = ref('none')
const sortBy = ref('state')

const stateLabels = taskStateLabels
const stateOptions = taskStateOptions

const stateTagClass = {
  0: 'is-light',
  1: 'is-danger',
  2: 'is-warning',
  3: 'is-success',
}

const selectedStates = ref(stateOptions.map((option) => option.value))

const taskModalOpen = ref(false)
const editingTask = ref(null)

const deleteTaskModalOpen = ref(false)
const deleteTaskTarget = ref(null)
const deleteTaskMessage = computed(() =>
  deleteTaskTarget.value ? `Delete "${deleteTaskTarget.value.title}"? This cannot be undone.` : '',
)

const completeTaskModalOpen = ref(false)
const completingTask = ref(null)

const displayOpen = ref(false)
const displayRef = ref(null)

function handleClickOutside(event) {
  if (displayOpen.value && displayRef.value && !displayRef.value.contains(event.target)) {
    displayOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', handleClickOutside))

async function fetchRoom() {
  loading.value = true
  error.value = null
  try {
    const response = await fetch(`/api/rooms/${props.id}`)
    if (!response.ok) throw new Error('Failed to load room')
    room.value = await response.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchRoom)
onMounted(() => roomsStore.fetchRooms())
watch(() => props.id, fetchRoom)

function openAddTaskModal() {
  editingTask.value = null
  taskModalOpen.value = true
}

function openEditTaskModal(task) {
  editingTask.value = task
  taskModalOpen.value = true
}

function closeTaskModal() {
  taskModalOpen.value = false
}

async function submitTask({ id, ...body }) {
  const url = id ? `/api/tasks/${id}` : '/api/tasks'
  const response = await fetch(url, {
    method: id ? 'PATCH' : 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!response.ok) return
  closeTaskModal()
  await fetchRoom()
}

function requestDeleteTask() {
  deleteTaskTarget.value = editingTask.value
  closeTaskModal()
  deleteTaskModalOpen.value = true
}

function closeDeleteTaskModal() {
  deleteTaskModalOpen.value = false
  deleteTaskTarget.value = null
}

async function confirmDeleteTask() {
  if (!deleteTaskTarget.value) return
  const response = await fetch(`/api/tasks/${deleteTaskTarget.value.id}`, { method: 'DELETE' })
  if (!response.ok) return
  closeDeleteTaskModal()
  await fetchRoom()
}

function openCompleteTaskModal(task) {
  completingTask.value = task
  completeTaskModalOpen.value = true
}

function closeCompleteTaskModal() {
  completeTaskModalOpen.value = false
  completingTask.value = null
}

async function confirmCompleteTask(payload) {
  if (!completingTask.value) return
  const response = await fetch(`/api/tasks/${completingTask.value.id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!response.ok) return
  closeCompleteTaskModal()
  await fetchRoom()
}

const filteredTasks = computed(() => {
  const tasks = room.value?.tasks ?? []
  const query = searchText.value.trim().toLowerCase()

  const filtered = tasks.filter((task) => {
    const matchesQuery = !query || task.title.toLowerCase().includes(query)
    const matchesState = selectedStates.value.includes(task.state)
    return matchesQuery && matchesState
  })

  return [...filtered].sort((a, b) => {
    switch (sortBy.value) {
      case 'lastPerformed':
        return new Date(b.last_performed) - new Date(a.last_performed)
      case 'lastInspected':
        return new Date(b.last_inspected) - new Date(a.last_inspected)
      case 'state':
        return a.state - b.state
      default:
        return a.title.localeCompare(b.title)
    }
  })
})

function formatDate(value) {
  return new Date(value).toLocaleDateString()
}
</script>

<template>
  <div class="room-view">
    <div class="room-view__header">
      <h1 class="title">{{ room?.title ?? 'Room' }}</h1>

      <div class="room-view__header-actions">
        <button class="button room-view__add-task" type="button" @click="openAddTaskModal">
          <font-awesome-icon :icon="['fas', 'plus']" size="sm" />
          <span>Add Task</span>
        </button>

        <button class="button" type="button">
          <span class="icon is-small">
            <font-awesome-icon :icon="['fas', 'magnifying-glass']" size="sm" />
          </span>
          <span>Inspect</span>
        </button>

        <div
          ref="displayRef"
          class="dropdown is-right room-view__display"
          :class="{ 'is-active': displayOpen }"
        >
          <div class="dropdown-trigger">
            <button
              class="button"
              type="button"
              aria-haspopup="true"
              aria-controls="display-dropdown-menu"
              @click="displayOpen = !displayOpen"
            >
              <span class="icon is-small">
                <font-awesome-icon :icon="['fas', 'sliders']" size="sm" />
              </span>
              <span>Display</span>
            </button>
          </div>
          <div id="display-dropdown-menu" class="dropdown-menu" role="menu">
            <div class="dropdown-content">
              <div class="dropdown-item">
                <p class="menu-label mb-2">Sort</p>

                <div class="field">
                  <label class="label is-small">Grouping</label>
                  <div class="control">
                    <div class="select is-small is-fullwidth">
                      <select v-model="groupBy">
                        <option value="none">None</option>
                      </select>
                    </div>
                  </div>
                </div>

                <div class="field">
                  <label class="label is-small">Sorting</label>
                  <div class="control">
                    <div class="select is-small is-fullwidth">
                      <select v-model="sortBy">
                        <option value="state">State</option>
                        <option value="name">Title</option>
                        <option value="lastPerformed">Last Performed</option>
                        <option value="lastInspected">Last Inspected</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>

              <hr class="dropdown-divider" />

              <div class="dropdown-item">
                <p class="menu-label mb-2">Filter</p>

                <div class="field">
                  <div class="control room-view__state-filter">
                    <label v-for="option in stateOptions" :key="option.value" class="checkbox">
                      <input v-model="selectedStates" type="checkbox" :value="option.value" />
                      {{ option.label }}
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="room-view__controls mb-3">
      <div class="field room-view__search">
        <div class="control has-icons-left">
          <input v-model="searchText" class="input" type="text" placeholder="Search tasks" />
          <span class="icon is-small is-left">
            <font-awesome-icon :icon="['fas', 'magnifying-glass']" size="sm" />
          </span>
        </div>
      </div>
    </div>

    <p v-if="error" class="notification is-danger">{{ error }}</p>

    <table v-else class="table is-fullwidth is-hoverable room-view__table">
      <thead>
        <tr>
          <th></th>
          <th>State</th>
          <th class="room-view__task-column">Task</th>
          <th>Last Performed</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in filteredTasks" :key="task.id" class="room-view__task-row">
          <td class="room-view__cell-middle room-view__actions">
            <span class="room-view__row-actions">
              <button class="button is-small is-text" type="button" title="Today">
                <font-awesome-icon :icon="['fas', 'calendar-day']" size="sm" />
              </button>
              <button
                class="button is-small is-text"
                type="button"
                title="Complete"
                @click="openCompleteTaskModal(task)"
              >
                <font-awesome-icon :icon="['fas', 'check']" size="sm" />
              </button>
              <button
                class="button is-small is-text"
                type="button"
                title="Edit"
                @click="openEditTaskModal(task)"
              >
                <font-awesome-icon :icon="['fas', 'pencil']" size="sm" />
              </button>
            </span>
          </td>
          <td class="room-view__cell-middle">
            <span class="tag room-view__state-tag" :class="stateTagClass[task.state]">
              {{ stateLabels[task.state] }}
            </span>
          </td>
          <td>
            <p>{{ task.title }}</p>
            <p v-if="task.description" class="room-view__task-description">
              {{ task.description }}
            </p>
          </td>
          <td class="room-view__cell-middle">{{ formatDate(task.last_performed) }}</td>
        </tr>
        <tr v-if="!loading && filteredTasks.length === 0">
          <td colspan="4" class="has-text-centered has-text-grey">No tasks found.</td>
        </tr>
      </tbody>
    </table>

    <TaskFormModal
      :open="taskModalOpen"
      :rooms="roomsStore.rooms"
      :default-room-id="Number(props.id)"
      :task="editingTask"
      @submit="submitTask"
      @close="closeTaskModal"
      @delete="requestDeleteTask"
    />

    <ConfirmModal
      :open="deleteTaskModalOpen"
      heading="Delete Task"
      :message="deleteTaskMessage"
      confirm-label="Delete"
      @confirm="confirmDeleteTask"
      @close="closeDeleteTaskModal"
    />

    <CompleteTaskModal
      :open="completeTaskModalOpen"
      @confirm="confirmCompleteTask"
      @close="closeCompleteTaskModal"
    />
  </div>
</template>

<style scoped>
.room-view {
  padding: 1rem 1.5rem 2rem;
}

.room-view__header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
}

.room-view__header .title {
  margin-bottom: 0;
}

.room-view__header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.room-view__actions {
  white-space: nowrap;
}

.room-view__row-actions {
  display: flex;
  gap: 0.25rem;
}

.room-view__task-row:hover .room-view__row-actions {
  display: flex;
}

.room-view__cell-middle {
  vertical-align: middle;
}

.room-view__task-description {
  font-size: 0.85em;
  font-style: italic;
  color: var(--bulma-text-weak);
}

.room-view__display .dropdown-menu {
  width: 16rem;
}

.room-view__task-column {
  width: 100%;
}

.room-view__table thead th {
  vertical-align: bottom;
}

.room-view__state-tag {
  width: 5.5rem;
}

.room-view__state-filter {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.room-view__controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-top: 1.75rem;
  margin-bottom: 1.5rem;
}

.field.room-view__search {
  flex: 1;
  min-width: 12rem;
  margin-bottom: 0;
}

.room-view__add-task {
  gap: 0.5rem;
  margin-left: auto;
}
</style>
