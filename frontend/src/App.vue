<template>
  <div class="app-shell">
    <AppHeader />
    <main class="page-shell">
      <RouterView />
    </main>
    <AppFooter />
    <ToastMessage />
  </div>
</template>

<script setup>
import AppFooter from '@/components/AppFooter.vue';
import AppHeader from '@/components/AppHeader.vue';
import ToastMessage from '@/components/ToastMessage.vue';
</script>

