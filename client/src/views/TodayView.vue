<script setup>
import { onMounted, ref } from 'vue'

import ScheduledTaskList from '@/components/ScheduledTaskList.vue'

const overdueTasks = ref([])
const todayTasks = ref([])
const loading = ref(false)
const error = ref(null)

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
</script>

<template>
  <div class="today-view">
    <h1 class="title">Today</h1>

    <p v-if="error" class="notification is-danger">{{ error }}</p>

    <template v-else>
      <section v-if="overdueTasks.length > 0" class="today-view__section">
        <h2 class="subtitle">Overdue</h2>
        <ScheduledTaskList :tasks="overdueTasks" :loading="loading" />
      </section>

      <section class="today-view__section">
        <h2 class="subtitle">Today</h2>
        <ScheduledTaskList
          :tasks="todayTasks"
          :loading="loading"
          empty-message="No tasks scheduled for today."
        />
      </section>
    </template>
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
