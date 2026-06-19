<template>
  <div>
    <header class="page-heading"><div><p class="eyebrow">Личная полка</p><h1>Избранные книги</h1><p>Сохранённые книги всегда под рукой.</p></div></header>
    <BookList :books="favorites" empty-title="В избранном пока пусто" empty-text="Нажмите на сердечко в каталоге, чтобы сохранить книгу." @favorite="toggleFavorite" @reserve="toggleReserve" @availability="toggleAvailability" @delete="confirmDelete" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import BookList from '@/components/BookList.vue';
import { useBooks } from '@/composables/useBooks';
const { favorites, loadBooks, toggleFavorite, toggleReserve, toggleAvailability, deleteBook } = useBooks();
onMounted(loadBooks);
function confirmDelete(book) { if (window.confirm(`Удалить книгу «${book.title}»?`)) deleteBook(book.id); }
</script>

