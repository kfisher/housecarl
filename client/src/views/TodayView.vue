<script setup>
import { onMounted, ref } from 'vue'

import { removeCompletedTaskFromLists } from '@/api/taskCompletion'
import CompleteTaskModal from '@/components/CompleteTaskModal.vue'
import ScheduledTaskList from '@/components/ScheduledTaskList.vue'

const overdueTasks = ref([])
const todayTasks = ref([])
const loading = ref(false)
const error = ref(null)

const completeTaskModalOpen = ref(false)
const completingTask = ref(null)

async function fetchScheduledTasks() {
  loading.value = true
  error.value = null
  try {
    const [overdueResponse, todayResponse] = await Promise.all([
      fetch('/api/scheduled-tasks/overdue'),
      fetch('/api/scheduled-tasks/today'),
    ])
    if (!overdueResponse.ok || !todayResponse.ok) {
      throw new Error('Failed to load scheduled tasks')
    }
    overdueTasks.value = await overdueResponse.json()
    todayTasks.value = await todayResponse.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchScheduledTasks)

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
  await removeCompletedTaskFromLists(completingTask.value.id)
  closeCompleteTaskModal()
  await fetchScheduledTasks()
}

async function removeTask(task) {
  const response = await fetch(`/api/scheduled-tasks/${task.id}`, { method: 'DELETE' })
  if (!response.ok) return
  await fetchScheduledTasks()
}
</script>

<template>
  <div class="today-view">
    <p v-if="error" class="notification is-danger">{{ error }}</p>

    <template v-else>
      <section v-if="overdueTasks.length > 0" class="today-view__section">
        <h1 class="title">Overdue</h1>
        <ScheduledTaskList
          :tasks="overdueTasks"
          :loading="loading"
          @complete="openCompleteTaskModal"
          @remove="removeTask"
        />
      </section>

      <section class="today-view__section">
        <h1 class="title">Today</h1>
        <ScheduledTaskList
          :tasks="todayTasks"
          :loading="loading"
          empty-message="No tasks scheduled for today."
          @complete="openCompleteTaskModal"
          @remove="removeTask"
        />
      </section>
    </template>

    <CompleteTaskModal
      :open="completeTaskModalOpen"
      :task-title="completingTask?.title"
      :room-title="completingTask?.room?.title"
      @confirm="confirmCompleteTask"
      @close="closeCompleteTaskModal"
    />
  </div>
</template>

<style scoped>
.today-view {
  padding: 1rem 1.5rem 2rem;
}

.today-view__section + .today-view__section {
  margin-top: 2rem;
}
</style>
