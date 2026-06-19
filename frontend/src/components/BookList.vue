<template>
  <div v-if="books.length" class="books-grid">
    <BookItem
      v-for="book in books"
      :key="book.id"
      :book="book"
      @favorite="$emit('favorite', $event)"
      @reserve="$emit('reserve', $event)"
      @availability="$emit('availability', $event)"
      @delete="$emit('delete', $event)"
    />
  </div>
  <div v-else class="empty-state">
    <span>⌕</span>
    <h3>{{ emptyTitle }}</h3>
    <p>{{ emptyText }}</p>
  </div>
</template>

<script setup>
import BookItem from './BookItem.vue';
defineProps({
  books: { type: Array, required: true },
  emptyTitle: { type: String, default: 'Книги не найдены' },
  emptyText: { type: String, default: 'Попробуйте изменить параметры фильтрации.' },
});
defineEmits(['favorite', 'reserve', 'availability', 'delete']);
</script>

