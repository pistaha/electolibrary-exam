<template>
  <div>
    <section class="hero">
      <div class="hero-copy">
        <p class="eyebrow">Ваша библиотека — в одном месте</p>
        <h1>Книги, к которым хочется возвращаться</h1>
        <p class="hero-lead">Управляйте каталогом, собирайте тематические подборки и бронируйте книги онлайн.</p>
        <div class="hero-actions">
          <RouterLink class="button button-primary" :to="{ name: 'books' }">Открыть каталог <span>→</span></RouterLink>
          <RouterLink class="button button-ghost" :to="{ name: 'book-new' }">Добавить книгу</RouterLink>
        </div>
        <div class="hero-stats">
          <div><strong>{{ total }}</strong><span>книг в каталоге</span></div>
          <div><strong>{{ available }}</strong><span>доступно сейчас</span></div>
          <div><strong>{{ collections.length }}</strong><span>подборки</span></div>
        </div>
      </div>
      <div class="hero-visual" aria-hidden="true">
        <div class="orbit orbit-one"></div><div class="orbit orbit-two"></div>
        <div class="floating-book book-one"><span>Э</span><small>Классика</small></div>
        <div class="floating-book book-two"><span>Л</span><small>Литература</small></div>
        <div class="floating-book book-three"><span>К</span><small>Коллекция</small></div>
      </div>
    </section>

    <section class="feature-section">
      <div class="section-heading"><p class="eyebrow">Возможности</p><h2>Простая работа с каталогом</h2></div>
      <div class="feature-grid">
        <LayoutCard v-for="feature in features" :key="feature.title" :meta-label="feature.meta">
          <template #header><span class="feature-icon">{{ feature.icon }}</span></template>
          <h3>{{ feature.title }}</h3><p>{{ feature.text }}</p>
          <template #meta="{ label }"><span>{{ label }}</span></template>
        </LayoutCard>
      </div>
    </section>

    <section v-if="favorites.length" class="home-favorites">
      <div class="section-heading inline"><div><p class="eyebrow">Избранное</p><h2>Ваши любимые книги</h2></div><RouterLink :to="{ name: 'favorites' }">Смотреть все →</RouterLink></div>
      <BookList :books="favorites.slice(0, 3)" @favorite="toggleFavorite" @reserve="toggleReserve" @availability="toggleAvailability" @delete="confirmDelete" />
    </section>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import BookList from '@/components/BookList.vue';
import LayoutCard from '@/components/LayoutCard.vue';
import { useBooks } from '@/composables/useBooks';

const { total, available, favorites, collections, loadBooks, toggleFavorite, toggleReserve, toggleAvailability, deleteBook } = useBooks();
const features = [
  { icon: '⌕', title: 'Умный каталог', text: 'Фильтруйте книги по статусу и находите нужное по названию или автору.', meta: 'Поиск и сортировка' },
  { icon: '♡', title: 'Личные списки', text: 'Отмечайте любимые книги и объединяйте их в тематические подборки.', meta: 'Избранное и коллекции' },
  { icon: '✓', title: 'Бронирование', text: 'Проверяйте доступность и резервируйте книгу одним действием.', meta: 'Актуальный статус' },
];
onMounted(loadBooks);
function confirmDelete(book) { if (window.confirm(`Удалить книгу «${book.title}»?`)) deleteBook(book.id); }
</script>

