<!--
Copyright 2026 Kevin Fisher. All rights reserved.
SPDX-License-Identifier: AGPL-3.0-only
-->

<script setup>
import { nextTick, ref, watch } from 'vue'

const props = defineProps({
  open: {
    type: Boolean,
    default: false,
  },
  heading: {
    type: String,
    required: true,
  },
  initialTitle: {
    type: String,
    default: '',
  },
  showDelete: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['submit', 'close', 'delete'])

const title = ref(props.initialTitle)
const inputRef = ref(null)

watch(
  () => props.open,
  async (isOpen) => {
    if (!isOpen) return
    title.value = props.initialTitle
    await nextTick()
    inputRef.value?.focus()
  },
)

function submit() {
  const trimmed = title.value.trim()
  if (!trimmed) return
  emit('submit', trimmed)
}
</script>

<template>
  <div class="modal" :class="{ 'is-active': open }">
    <div class="modal-background" @click="emit('close')"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">{{ heading }}</p>
        <button class="delete" aria-label="close" type="button" @click="emit('close')"></button>
      </header>
      <section class="modal-card-body">
        <div class="field">
          <label class="label">Room name</label>
          <div class="control">
            <input
              ref="inputRef"
              v-model="title"
              class="input"
              type="text"
              @keyup.enter="submit"
              @keyup.esc="emit('close')"
            />
          </div>
        </div>
      </section>
      <footer class="modal-card-foot room-form-modal__foot">
        <button
          v-if="showDelete"
          class="button is-danger is-light"
          type="button"
          @click="emit('delete')"
        >
          Delete
        </button>
        <div class="buttons room-form-modal__save-cancel">
          <button class="button is-primary" type="button" @click="submit">Save</button>
          <button class="button" type="button" @click="emit('close')">Cancel</button>
        </div>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.room-form-modal__foot {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.room-form-modal__save-cancel {
  margin-left: auto;
}
</style>
