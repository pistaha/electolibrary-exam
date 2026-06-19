<template>
  <article class="book-card">
    <button class="heart" :class="{ active: book.favorite }" type="button" :aria-label="book.favorite ? 'Убрать из избранного' : 'В избранное'" @click="$emit('favorite', book)">
      {{ book.favorite ? '♥' : '♡' }}
    </button>
    <div class="book-cover-wrap">
      <img v-if="book.cover_url" class="book-cover" :src="book.cover_url" :alt="`Обложка книги ${book.title}`" />
      <div v-else class="book-cover book-cover-empty"><span>{{ initials }}</span></div>
    </div>
    <div class="book-content">
      <div class="book-tags">
        <span class="tag">{{ book.age_rating }}</span>
        <span :class="['status', book.available ? 'available' : 'unavailable']">{{ book.available ? 'В наличии' : 'Недоступна' }}</span>
      </div>
      <h3>{{ book.title }}</h3>
      <p class="book-author">{{ book.author }}</p>
      <p class="book-description">{{ book.description }}</p>
      <dl class="book-details">
        <div><dt>Издательство</dt><dd>{{ book.publisher }}</dd></div>
        <div><dt>Год</dt><dd>{{ book.publication_year }}</dd></div>
      </dl>
      <p v-if="book.collection_name" class="collection-label">Подборка: {{ book.collection_name }}</p>
      <div class="book-actions">
        <button class="button button-small button-primary" type="button" :disabled="!book.available && !book.reserved" @click="$emit('reserve', book)">
          {{ book.reserved ? 'Отменить бронь' : 'Забронировать' }}
        </button>
        <RouterLink class="button button-small button-light" :to="{ name: 'book-edit', params: { id: book.id } }">Редактировать</RouterLink>
        <button class="icon-button" type="button" aria-label="Изменить статус" title="Изменить статус" @click="$emit('availability', book)">↻</button>
        <button class="icon-button danger" type="button" aria-label="Удалить книгу" title="Удалить" @click="$emit('delete', book)">×</button>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({ book: { type: Object, required: true } });
defineEmits(['favorite', 'reserve', 'availability', 'delete']);
const initials = computed(() => props.book.title.split(/\s+/).slice(0, 2).map((word) => word[0]).join('').toUpperCase());
</script>

