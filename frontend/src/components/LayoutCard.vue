<template>
  <section class="layout-card">
    <header v-if="$slots.header" class="layout-card-header"><slot name="header" /></header>
    <div class="layout-card-body"><slot /></div>
    <div v-if="$slots.meta" class="layout-card-meta">
      <slot name="meta" :label="metaLabel" :accent="accent" />
    </div>
    <footer v-if="$slots.footer" class="layout-card-footer"><slot name="footer" /></footer>
  </section>
</template>

<script setup>
defineProps({ metaLabel: { type: String, default: '' }, accent: { type: String, default: 'teal' } });
</script>

