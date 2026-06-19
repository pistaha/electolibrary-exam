<template>
  <div>
    <header class="page-heading"><div><p class="eyebrow">Тематические списки</p><h1>Подборки книг</h1><p>Объединяйте каталог по темам, курсам или настроению.</p></div></header>
    <div v-if="collections.length" class="collection-sections">
      <LayoutCard v-for="name in collections" :key="name" :meta-label="`${grouped[name].length} книг`">
        <template #header><div class="collection-heading"><span>✦</span><h2>{{ name }}</h2></div></template>
        <ul class="collection-list">
          <li v-for="book in grouped[name]" :key="book.id"><div><strong>{{ book.title }}</strong><span>{{ book.author }}</span></div><button class="text-button" type="button" @click="setCollection(book, '')">Убрать</button></li>
        </ul>
        <template #meta="{ label }"><span>{{ label }}</span></template>
      </LayoutCard>
    </div>
    <div v-else class="empty-state"><span>✦</span><h3>Подборок пока нет</h3><p>Укажите подборку при создании или редактировании книги.</p></div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import LayoutCard from '@/components/LayoutCard.vue';
import { useBooks } from '@/composables/useBooks';
const { state, collections, loadBooks, setCollection } = useBooks();
const grouped = computed(() => Object.fromEntries(collections.value.map((name) => [name, state.books.filter((book) => book.collection_name === name)])));
onMounted(loadBooks);
</script>

