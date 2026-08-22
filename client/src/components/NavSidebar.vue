<script setup>
import { computed, onMounted, ref } from 'vue'

import ConfirmModal from '@/components/ConfirmModal.vue'
import RoomFormModal from '@/components/RoomFormModal.vue'
import { useRoomsStore } from '@/stores/rooms'

const roomsStore = useRoomsStore()

const modalOpen = ref(false)
const modalMode = ref('add')
const modalRoom = ref(null)

const deleteModalOpen = ref(false)
const deleteTarget = ref(null)

const modalHeading = computed(() => (modalMode.value === 'add' ? 'Add Room' : 'Edit Room'))
const deleteMessage = computed(() =>
  deleteTarget.value ? `Delete "${deleteTarget.value.title}"? This cannot be undone.` : '',
)

onMounted(() => {
  roomsStore.fetchRooms()
})

function openAddModal() {
  modalMode.value = 'add'
  modalRoom.value = null
  modalOpen.value = true
}

function openEditModal(room) {
  modalMode.value = 'edit'
  modalRoom.value = room
  modalOpen.value = true
}

function closeModal() {
  modalOpen.value = false
}

async function submitModal(title) {
  if (modalMode.value === 'add') {
    await roomsStore.addRoom(title)
  } else {
    await roomsStore.updateRoom(modalRoom.value.id, title)
  }
  closeModal()
}

function requestDelete() {
  deleteTarget.value = modalRoom.value
  modalOpen.value = false
  deleteModalOpen.value = true
}

function closeDeleteModal() {
  deleteModalOpen.value = false
  deleteTarget.value = null
}

async function confirmDelete() {
  if (!deleteTarget.value) return
  await roomsStore.removeRoom(deleteTarget.value.id)
  closeDeleteModal()
}
</script>

<template>
  <aside class="menu nav-sidebar">
    <ul class="menu-list">
      <li>
        <div class="nav-sidebar__row">
          <router-link to="/" active-class="is-active">Today</router-link>
        </div>
      </li>
      <li>
        <div class="nav-sidebar__row">
          <router-link to="/random" active-class="is-active">Random</router-link>
        </div>
      </li>
    </ul>

    <p class="menu-label">Rooms</p>

    <ul class="menu-list">
      <li v-for="room in roomsStore.rooms" :key="room.id">
        <div class="nav-sidebar__row">
          <router-link :to="`/rooms/${room.id}`" active-class="is-active">
            {{ room.title }}
          </router-link>
          <span class="nav-sidebar__row-controls">
            <button
              class="button is-small is-text"
              type="button"
              title="Edit room"
              @click="openEditModal(room)"
            >
              <font-awesome-icon :icon="['fas', 'pen']" size="sm" />
            </button>
          </span>
        </div>
      </li>
    </ul>

    <button class="button is-fullwidth nav-sidebar__add-room" type="button" @click="openAddModal">
      <font-awesome-icon :icon="['fas', 'plus']" size="sm" />
      <span>Add Room</span>
    </button>

    <RoomFormModal
      :open="modalOpen"
      :heading="modalHeading"
      :initial-title="modalRoom?.title ?? ''"
      :show-delete="modalMode === 'edit'"
      @submit="submitModal"
      @close="closeModal"
      @delete="requestDelete"
    />

    <ConfirmModal
      :open="deleteModalOpen"
      heading="Delete Room"
      :message="deleteMessage"
      confirm-label="Delete"
      @confirm="confirmDelete"
      @close="closeDeleteModal"
    />
  </aside>
</template>

<style scoped>
.nav-sidebar {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 0.5rem 0.25rem;
}

.nav-sidebar__add-room {
  margin-top: auto;
  gap: 0.5rem;
}

.nav-sidebar__row {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  border-radius: var(--bulma-radius-small);
}

.nav-sidebar__row a {
  line-height: var(--bulma-control-line-height);
}

.nav-sidebar__row a,
.nav-sidebar__row button {
  background-color: transparent !important;
}

.nav-sidebar__row:hover {
  background-color: var(--bulma-background-hover);
}

.nav-sidebar__row:has(.is-active) {
  background-color: var(--bulma-link);
}

.nav-sidebar__row:has(.is-active) a,
.nav-sidebar__row:has(.is-active) button {
  color: var(--bulma-link-invert) !important;
}

.nav-sidebar__row a {
  flex: 1;
}

.nav-sidebar__row-controls {
  display: none;
  gap: 0.25rem;
}

.nav-sidebar__row:hover .nav-sidebar__row-controls {
  display: flex;
}

.nav-sidebar__row .nav-sidebar__row-controls .button:hover {
  background-color: var(--bulma-background) !important;
}

.nav-sidebar__row:has(.is-active) .nav-sidebar__row-controls .button:hover {
  background-color: var(--bulma-link-60) !important;
}
</style>
