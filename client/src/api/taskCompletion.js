/**
 * Removes a completed task from the scheduled and random task lists, if
 * it was present on either. The random task's slot, if any, is
 * replaced by the server with another eligible task.
 */
export async function removeCompletedTaskFromLists(taskId) {
  await Promise.all([
    fetch(`/api/scheduled-tasks/${taskId}`, { method: 'DELETE' }),
    fetch(`/api/random-tasks/${taskId}`, { method: 'DELETE' }),
  ])
}
