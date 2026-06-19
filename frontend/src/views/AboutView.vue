<template>
  <div class="about-page">
    <header class="page-heading"><div><p class="eyebrow">Итоговое задание</p><h1>О проекте</h1><p>SPA-приложение электронной библиотеки, созданное на Vue 3 и FastAPI.</p></div></header>
    <div class="about-grid">
      <LayoutCard meta-label="Frontend">
        <template #header><h2>Vue 3</h2></template>
        <p>Composition API, реактивные данные, computed и watch, компоненты, props, события, формы и Vue Router.</p>
        <template #meta="{ label }"><span class="tech-pill">{{ label }}</span></template>
      </LayoutCard>
      <LayoutCard meta-label="Backend">
        <template #header><h2>FastAPI + SQLite</h2></template>
        <p>REST API с CRUD-операциями, постоянным хранением данных и интерактивной документацией.</p>
        <template #meta="{ label }"><span class="tech-pill">{{ label }}</span></template>
      </LayoutCard>
      <LayoutCard meta-label="Infrastructure">
        <template #header><h2>Docker</h2></template>
        <p>Отдельные контейнеры frontend и backend, nginx-прокси и том для базы данных.</p>
        <template #meta="{ label }"><span class="tech-pill">{{ label }}</span></template>
      </LayoutCard>
    </div>
    <LayoutCard>
      <template #header><h2>Автор</h2></template>
      <div class="author-card"><div class="author-avatar">ЯР</div><div><strong>Ярослав Рыбаков</strong><p>Группа P3269 · 19 июня 2026</p></div></div>
      <template #footer><RouterLink class="button button-primary" :to="{ name: 'books' }">Перейти в каталог</RouterLink></template>
    </LayoutCard>
  </div>
</template>

<script setup>import LayoutCard from '@/components/LayoutCard.vue';</script>

