<template>
  <header class="site-header">
    <div class="header-inner">
      <RouterLink class="brand" :to="{ name: 'home' }">
        <span class="brand-mark">E</span>
        <span>ElectoLibrary</span>
      </RouterLink>
      <button class="menu-button" type="button" aria-label="Открыть меню" @click="open = !open">☰</button>
      <nav :class="['main-nav', { open }]" aria-label="Основная навигация" @click="open = false">
        <RouterLink :to="{ name: 'home' }">Главная</RouterLink>
        <RouterLink :to="{ name: 'books' }">Каталог</RouterLink>
        <RouterLink :to="{ name: 'favorites' }">Избранное</RouterLink>
        <RouterLink :to="{ name: 'collections' }">Подборки</RouterLink>
        <RouterLink :to="{ name: 'about' }">О проекте</RouterLink>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';
const open = ref(false);
</script>

