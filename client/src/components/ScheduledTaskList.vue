<script setup>
import { taskStateLabels } from '@/constants/taskState'

defineProps({
  tasks: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  emptyMessage: {
    type: String,
    default: 'No tasks.',
  },
})

const stateLabels = taskStateLabels

const stateTagClass = {
  0: 'is-light',
  1: 'is-danger',
  2: 'is-warning',
  3: 'is-success',
}
</script>

<template>
  <table class="table is-fullwidth is-hoverable scheduled-task-list">
    <tbody>
      <tr v-for="entry in tasks" :key="entry.id" class="scheduled-task-list__row">
        <td class="scheduled-task-list__cell-middle scheduled-task-list__actions">
          <span class="scheduled-task-list__row-actions">
            <button class="button is-small is-text" type="button" title="Remove">
              <font-awesome-icon :icon="['fas', 'xmark']" size="sm" />
            </button>
            <button class="button is-small is-text" type="button" title="Complete">
              <font-awesome-icon :icon="['fas', 'check']" size="sm" />
            </button>
          </span>
        </td>
        <td class="scheduled-task-list__cell-middle">
          <span class="tag scheduled-task-list__state-tag" :class="stateTagClass[entry.task.state]">
            {{ stateLabels[entry.task.state] }}
          </span>
        </td>
        <td class="scheduled-task-list__cell-middle scheduled-task-list__room">
          {{ entry.task.room.title }}
        </td>
        <td class="scheduled-task-list__task-column">
          <p>{{ entry.task.title }}</p>
          <p v-if="entry.task.description" class="scheduled-task-list__task-description">
            {{ entry.task.description }}
          </p>
        </td>
      </tr>
      <tr v-if="!loading && tasks.length === 0">
        <td colspan="4" class="has-text-centered has-text-grey">{{ emptyMessage }}</td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
.scheduled-task-list__row-actions {
  display: flex;
  gap: 0.25rem;
}

.scheduled-task-list__cell-middle {
  vertical-align: middle;
}

.scheduled-task-list__actions {
  white-space: nowrap;
}

.scheduled-task-list__room {
  width: 1%;
  white-space: nowrap;
}

.scheduled-task-list__task-column {
  width: 100%;
}

.scheduled-task-list__task-description {
  font-size: 0.85em;
  font-style: italic;
  color: var(--bulma-text-weak);
}

.scheduled-task-list__state-tag {
  width: 5.5rem;
}
</style>
