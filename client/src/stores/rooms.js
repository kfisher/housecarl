// Copyright 2026 Kevin Fisher. All rights reserved.
// SPDX-License-Identifier: AGPL-3.0-only

import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useRoomsStore = defineStore('rooms', () => {
  const rooms = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchRooms() {
    loading.value = true
    error.value = null
    try {
      const response = await fetch('/api/rooms')
      if (!response.ok) throw new Error('Failed to load rooms')
      rooms.value = await response.json()
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function addRoom(title) {
    const response = await fetch('/api/rooms', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title }),
    })
    if (!response.ok) throw new Error('Failed to create room')
    const room = await response.json()
    rooms.value.push(room)
    return room
  }

  async function updateRoom(id, title) {
    const response = await fetch(`/api/rooms/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title }),
    })
    if (!response.ok) throw new Error('Failed to update room')
    const room = await response.json()
    const index = rooms.value.findIndex((existing) => existing.id === id)
    if (index !== -1) rooms.value[index] = room
    return room
  }

  async function removeRoom(id) {
    const response = await fetch(`/api/rooms/${id}`, { method: 'DELETE' })
    if (!response.ok) throw new Error('Failed to delete room')
    rooms.value = rooms.value.filter((room) => room.id !== id)
  }

  return { rooms, loading, error, fetchRooms, addRoom, updateRoom, removeRoom }
})
