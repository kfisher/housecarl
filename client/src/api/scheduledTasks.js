// Copyright 2026 Kevin Fisher. All rights reserved.
// SPDX-License-Identifier: AGPL-3.0-only

/**
 * Schedules a task for the current day.
 */
export async function scheduleTaskToday(taskId) {
  return fetch(`/api/scheduled-tasks/${taskId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ date: new Date().toISOString() }),
  })
}

/**
 * Returns the ids of all tasks that currently have a scheduled entry.
 */
export async function fetchScheduledTaskIds() {
  const response = await fetch('/api/scheduled-tasks')
  if (!response.ok) return new Set()
  const scheduled = await response.json()
  return new Set(scheduled.map((entry) => entry.task.id))
}
