<!--
Copyright 2026 Kevin Fisher. All rights reserved.
SPDX-License-Identifier: AGPL-3.0-only
-->

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import { createTaskNote, deleteTaskNote, fetchTaskNotes } from '@/api/taskNotes'
import ConfirmModal from '@/components/ConfirmModal.vue'
import TaskFormModal from '@/components/TaskFormModal.vue'
import { taskStateLabels } from '@/constants/taskState'
import { useRoomsStore } from '@/stores/rooms'
import { formatFrequency } from '@/utils/frequency'

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
  taskId: {
    type: String,
    required: true,
  },
})

const router = useRouter()
const roomsStore = useRoomsStore()

const task = ref(null)
const loading = ref(false)
const error = ref(null)

const notes = ref([])
const notesLoaded = ref(false)

const stateLabels = taskStateLabels
const stateTagClass = {
  0: 'is-light',
  1: 'is-danger',
  2: 'is-warning',
  3: 'is-success',
}

const taskModalOpen = ref(false)
const deleteModalOpen = ref(false)

const newNoteText = ref('')

const noteDeleteModalOpen = ref(false)
const noteToDelete = ref(null)

const roomTitle = computed(
  () => roomsStore.rooms.find((room) => room.id === Number(props.id))?.title,
)

async function fetchTask() {
  loading.value = true
  error.value = null
  try {
    const response = await fetch(`/api/tasks/${props.taskId}`)
    if (!response.ok) throw new Error('Failed to load task')
    task.value = await response.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

async function fetchNotes() {
  notes.value = await fetchTaskNotes(props.taskId)
  notesLoaded.value = true
}

onMounted(fetchTask)
onMounted(fetchNotes)
onMounted(() => roomsStore.fetchRooms())
watch(() => props.taskId, () => {
  fetchTask()
  notesLoaded.value = false
  fetchNotes()
})

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

function openEditModal() {
  taskModalOpen.value = true
}

function closeTaskModal() {
  taskModalOpen.value = false
}

async function submitTask(body) {
  const response = await fetch(`/api/tasks/${body.id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: body.title,
      description: body.description,
      frequency: body.frequency,
      state: body.state,
      room_id: body.room_id,
    }),
  })
  if (!response.ok) return
  closeTaskModal()
  if (body.room_id !== Number(props.id)) {
    router.replace({ name: 'task', params: { id: body.room_id, taskId: body.id } })
  } else {
    await fetchTask()
  }
}

function openDeleteModal() {
  deleteModalOpen.value = true
}

function closeDeleteModal() {
  deleteModalOpen.value = false
}

async function confirmDelete() {
  const response = await fetch(`/api/tasks/${task.value.id}`, { method: 'DELETE' })
  if (!response.ok) return
  router.push({ name: 'room', params: { id: props.id } })
}

async function addNote() {
  const text = newNoteText.value.trim()
  if (!text) return
  const note = await createTaskNote(props.taskId, text)
  notes.value = [note, ...notes.value]
  newNoteText.value = ''
}

function openDeleteNoteModal(note) {
  noteToDelete.value = note
  noteDeleteModalOpen.value = true
}

function closeDeleteNoteModal() {
  noteDeleteModalOpen.value = false
  noteToDelete.value = null
}

async function confirmDeleteNote() {
  if (!noteToDelete.value) return
  await deleteTaskNote(noteToDelete.value.id)
  notes.value = notes.value.filter((note) => note.id !== noteToDelete.value.id)
  closeDeleteNoteModal()
}
</script>

<template>
  <div class="task-view">
    <template v-if="!loading && !error && task">
      <div class="task-view__task">
        <div class="task-view__title-row">
          <div class="tag task-view__state-tag mt-1" :class="stateTagClass[task.state]">
            {{ stateLabels[task.state] }}
          </div>
          <h1 class="title">{{ task.title }}</h1>
          <div class="task-view__toolbar-actions">
            <button class="button" type="button" @click="openEditModal">
              <span class="icon is-small">
                <font-awesome-icon :icon="['fas', 'pencil']" size="sm" />
              </span>
              <span>Edit</span>
            </button>
            <button class="button" type="button" @click="openDeleteModal">
              <span class="icon is-small">
                <font-awesome-icon :icon="['fas', 'trash']" size="sm" />
              </span>
              <span>Delete</span>
            </button>
          </div>
        </div>

        <p v-if="task.description" class="task-view__description">
          {{ task.description }}
        </p>

        <div class="task-view__meta">
          <p>
            <strong>Room</strong><br />
            {{ roomTitle }}
          </p>
          <p class="ml-5">
            <strong>Last Inspected</strong><br />
            {{ formatDate(task.last_inspected) }}
          </p>
          <p class="ml-5">
            <strong>Last Performed</strong><br />
            {{ formatDate(task.last_performed) }}
          </p>
          <p class="ml-5">
            <strong>Frequency</strong><br />
            {{ formatFrequency(task.frequency) }}
          </p>
        </div>

        <div class="task-view__notes-list">
          <p class="label">Notes</p>

          <div class="field">
            <div class="control">
              <textarea
                v-model="newNoteText"
                class="textarea"
                rows="2"
                placeholder="Add a note"
              ></textarea>
            </div>
          </div>
          <div class="buttons">
            <button
              class="button is-primary"
              type="button"
              :disabled="!newNoteText.trim()"
              @click="addNote"
            >
              Add Note
            </button>
          </div>

          <p v-if="!notesLoaded" class="has-text-grey">Loading notes…</p>
          <p v-else-if="notes.length === 0" class="has-text-grey">No notes yet.</p>
          <div v-for="note in notes" :key="note.id" class="task-view__note">
            <div class="task-view__note-header">
              <p class="task-view__note-date">{{ formatDate(note.date) }}</p>
              <button
                class="button is-small is-text"
                type="button"
                title="Delete note"
                @click="openDeleteNoteModal(note)"
              >
                <font-awesome-icon :icon="['fas', 'trash']" size="sm" />
              </button>
            </div>
            <p>{{ note.text }}</p>
          </div>
        </div>
      </div>
    </template>

    <TaskFormModal
      :open="taskModalOpen"
      :rooms="roomsStore.sortedRooms"
      :default-room-id="Number(props.id)"
      :task="task"
      @submit="submitTask"
      @close="closeTaskModal"
    />

    <ConfirmModal
      :open="deleteModalOpen"
      heading="Delete Task"
      :message="`Delete &quot;${task?.title}&quot;? This cannot be undone.`"
      confirm-label="Delete"
      @confirm="confirmDelete"
      @close="closeDeleteModal"
    />

    <ConfirmModal
      :open="noteDeleteModalOpen"
      heading="Delete Note"
      message="Delete this note? This cannot be undone."
      confirm-label="Delete"
      @confirm="confirmDeleteNote"
      @close="closeDeleteNoteModal"
    />
  </div>
</template>

<style scoped>
.task-view {
  padding: 1rem 1.5rem 2rem;
}

.task-view__toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.task-view__toolbar-actions {
  display: flex;
  gap: 0.5rem;
}

.task-view__title-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.task-view__title-row .title {
  margin-bottom: 0;
  flex: 1;
}

.task-view__state-tag {
  flex-shrink: 0;
  min-height: 32px;
  min-width: 72px;
}

.task-view__description {
  color: var(--bulma-text-weak);
  margin-top: 0.75rem;
  margin-bottom: 1rem;
}

.task-view__meta {
  margin-bottom: 1.5rem;
  margin-top: 1.5rem;
  font-size: 0.9em;
  display: flex;
}

.task-view__notes-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.task-view__note {
  border-top: 1px solid var(--bulma-border);
  padding-top: 0.5rem;
}

.task-view__note-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.task-view__note-date {
  font-size: 0.8em;
  color: var(--bulma-text-weak);
}
</style>
