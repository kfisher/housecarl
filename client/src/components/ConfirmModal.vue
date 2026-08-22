<script setup>
defineProps({
  open: {
    type: Boolean,
    default: false,
  },
  heading: {
    type: String,
    required: true,
  },
  message: {
    type: String,
    required: true,
  },
  confirmLabel: {
    type: String,
    default: 'Confirm',
  },
  cancelLabel: {
    type: String,
    default: 'Cancel',
  },
})

const emit = defineEmits(['confirm', 'close'])
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
        <p>{{ message }}</p>
      </section>
      <footer class="modal-card-foot confirm-modal__foot">
        <div class="buttons">
          <button class="button is-danger" type="button" @click="emit('confirm')">
            {{ confirmLabel }}
          </button>
          <button class="button" type="button" @click="emit('close')">
            {{ cancelLabel }}
          </button>
        </div>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.confirm-modal__foot {
  justify-content: flex-end;
}
</style>
