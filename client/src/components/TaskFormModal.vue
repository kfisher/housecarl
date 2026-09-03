<!--
Copyright 2026 Kevin Fisher. All rights reserved.
SPDX-License-Identifier: AGPL-3.0-only
-->

<script setup>
import { computed, nextTick, ref, watch } from 'vue'

import { defaultFrequencyUnit, frequencyUnitOptions } from '@/constants/frequencyUnit'
import { taskStateOptions } from '@/constants/taskState'
import { parseFrequency } from '@/utils/frequency'

const props = defineProps({
  open: {
    type: Boolean,
    default: false,
  },
  rooms: {
    type: Array,
    default: () => [],
  },
  defaultRoomId: {
    type: Number,
    required: true,
  },
  task: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['submit', 'close'])

const title = ref('')
const description = ref('')
const frequencyValue = ref(1)
const frequencyUnit = ref(defaultFrequencyUnit)
const state = ref(taskStateOptions[0].value)
const roomId = ref(props.defaultRoomId)
const titleInputRef = ref(null)
const attemptedSubmit = ref(false)

const heading = computed(() => (props.task ? 'Edit Task' : 'Add Task'))

const isTitleValid = computed(() => title.value.trim().length > 0)
const isFrequencyValid = computed(
  () => Number.isInteger(frequencyValue.value) && frequencyValue.value >= 1,
)
const isRoomValid = computed(() => roomId.value != null)

watch(
  () => props.open,
  async (isOpen) => {
    if (!isOpen) return
    if (props.task) {
      title.value = props.task.title
      description.value = props.task.description ?? ''
      const frequency = parseFrequency(props.task.frequency)
      frequencyValue.value = frequency.value
      frequencyUnit.value = frequency.unit
      state.value = props.task.state
    } else {
      title.value = ''
      description.value = ''
      frequencyValue.value = 1
      frequencyUnit.value = defaultFrequencyUnit
      state.value = taskStateOptions[0].value
    }
    roomId.value = props.defaultRoomId
    attemptedSubmit.value = false
    await nextTick()
    titleInputRef.value?.focus()
  },
)

function submit() {
  attemptedSubmit.value = true
  if (!isTitleValid.value || !isFrequencyValid.value || !isRoomValid.value) return

  emit('submit', {
    id: props.task?.id,
    title: title.value.trim(),
    description: description.value.trim() || null,
    frequency: `P${frequencyValue.value}${frequencyUnit.value}`,
    state: state.value,
    room_id: roomId.value,
  })
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
          <label class="label">Room</label>
          <div class="control">
            <div
              class="select is-fullwidth"
              :class="{ 'is-danger': attemptedSubmit && !isRoomValid }"
            >
              <select v-model.number="roomId">
                <option v-for="room in rooms" :key="room.id" :value="room.id">
                  {{ room.title }}
                </option>
              </select>
            </div>
          </div>
          <p v-if="attemptedSubmit && !isRoomValid" class="help is-danger">A room is required.</p>
        </div>

        <div class="field">
          <label class="label">Title</label>
          <div class="control">
            <input
              ref="titleInputRef"
              v-model="title"
              class="input"
              :class="{ 'is-danger': attemptedSubmit && !isTitleValid }"
              type="text"
              @keyup.esc="emit('close')"
            />
          </div>
          <p v-if="attemptedSubmit && !isTitleValid" class="help is-danger">Title is required.</p>
        </div>

        <div class="field">
          <label class="label">Description</label>
          <div class="control">
            <textarea v-model="description" class="textarea" rows="3"></textarea>
          </div>
        </div>

        <div class="field">
          <label class="label">Frequency</label>
          <div class="field has-addons">
            <div class="control is-expanded">
              <input
                v-model.number="frequencyValue"
                class="input"
                :class="{ 'is-danger': attemptedSubmit && !isFrequencyValid }"
                type="number"
                min="1"
                step="1"
              />
            </div>
            <div class="control">
              <div class="select">
                <select v-model="frequencyUnit">
                  <option
                    v-for="option in frequencyUnitOptions"
                    :key="option.value"
                    :value="option.value"
                  >
                    {{ option.label }}
                  </option>
                </select>
              </div>
            </div>
          </div>
          <p v-if="attemptedSubmit && !isFrequencyValid" class="help is-danger">
            Enter a frequency of at least 1.
          </p>
        </div>

        <div class="field">
          <label class="label">State</label>
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model.number="state">
                <option
                  v-for="option in taskStateOptions"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </section>
      <footer class="modal-card-foot task-form-modal__foot">
        <div class="buttons">
          <button class="button is-primary" type="button" @click="submit">Save</button>
          <button class="button" type="button" @click="emit('close')">Cancel</button>
        </div>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.modal-card-head {
  box-shadow: none;
}

.modal-card-foot {
  background-color: var(--bulma-scheme-main);
}

.task-form-modal__foot {
  justify-content: flex-end;
}
</style>
