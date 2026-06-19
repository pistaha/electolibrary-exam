<template>
  <div>
    <header class="page-heading">
      <div><p class="eyebrow">Электронный каталог</p><h1>Книги библиотеки</h1><p>Найдите книгу, измените её статус или добавьте новую запись.</p></div>
      <RouterLink class="button button-primary" :to="{ name: 'book-new' }">＋ Добавить книгу</RouterLink>
    </header>

    <section class="toolbar">
      <label class="search-field"><span>⌕</span><input ref="searchInput" v-model.trim="search" type="search" placeholder="Название или автор" /></label>
      <label><span>Статус</span><select v-model="status"><option value="all">Все книги</option><option value="available">В наличии</option><option value="unavailable">Недоступны</option></select></label>
      <label><span>Сортировка</span><select v-model="sort"><option value="newest">Сначала новые</option><option value="title">По алфавиту</option></select></label>
      <p class="results-count">Найдено: <strong>{{ filteredBooks.length }}</strong></p>
    </section>

    <div v-if="state.loading" class="loading">Загружаем каталог…</div>
    <div v-else-if="state.error" class="form-alert">{{ state.error }}</div>
    <BookList v-else :books="filteredBooks" @favorite="toggleFavorite" @reserve="toggleReserve" @availability="toggleAvailability" @delete="confirmDelete" />
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue';
import BookList from '@/components/BookList.vue';
import { useBooks } from '@/composables/useBooks';

const { state, loadBooks, toggleFavorite, toggleReserve, toggleAvailability, deleteBook } = useBooks();
const search = ref('');
const status = ref('all');
const sort = ref('newest');
const searchInput = ref(null);

const filteredBooks = computed(() => {
  const query = search.value.toLocaleLowerCase('ru');
  const books = state.books.filter((book) => {
    const matchesSearch = [book.title, book.author, book.publisher].some((value) => value.toLocaleLowerCase('ru').includes(query));
    const matchesStatus = status.value === 'all' || (status.value === 'available' ? book.available : !book.available);
    return matchesSearch && matchesStatus;
  });
  return [...books].sort((a, b) => sort.value === 'title' ? a.title.localeCompare(b.title, 'ru') : new Date(b.created_at) - new Date(a.created_at));
});

watch(search, (value) => { document.title = value ? `${value} — ElectoLibrary` : 'Каталог — ElectoLibrary'; });
onMounted(async () => { await loadBooks(); await nextTick(); searchInput.value?.focus(); });
function confirmDelete(book) { if (window.confirm(`Удалить книгу «${book.title}»?`)) deleteBook(book.id); }
</script>

