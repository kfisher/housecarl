/**
 * Returns the notes for a task, newest first.
 */
export async function fetchTaskNotes(taskId) {
  const response = await fetch(`/api/task-notes?task_id=${taskId}`)
  if (!response.ok) throw new Error('Failed to load task notes')
  return response.json()
}

/**
 * Adds a new note to a task.
 */
export async function createTaskNote(taskId, text) {
  const response = await fetch('/api/task-notes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task_id: taskId, text }),
  })
  if (!response.ok) throw new Error('Failed to add task note')
  return response.json()
}
