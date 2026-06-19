<template>
  <Transition name="toast">
    <div v-if="state.toast" class="toast" role="status">{{ state.toast }}</div>
  </Transition>
</template>

<script setup>
import { useBooks } from '@/composables/useBooks';
const { state } = useBooks();
</script>

