<template>
  <div>
    <header class="page-heading compact">
      <div><p class="eyebrow">{{ editing ? 'Редактирование' : 'Новая запись' }}</p><h1>{{ editing ? 'Изменить книгу' : 'Добавить книгу' }}</h1><p>Заполните библиографические данные по ГОСТ Р 7.0.100–2018.</p></div>
    </header>
    <LayoutCard>
      <template #header><h2>Библиографическая карточка</h2></template>
      <div v-if="loading" class="loading">Загружаем данные…</div>
      <BookForm v-else :initial="book" :saving="saving" :collections="collections" :submit-label="editing ? 'Сохранить изменения' : 'Добавить в каталог'" @submit="save" @cancel="router.push({ name: 'books' })" />
      <template #footer><p class="form-note">Поля, отмеченные звёздочкой, обязательны.</p></template>
    </LayoutCard>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import BookForm from '@/components/BookForm.vue';
import LayoutCard from '@/components/LayoutCard.vue';
import { useBooks } from '@/composables/useBooks';

const route = useRoute();
const router = useRouter();
const { state, collections, loadBooks, createBook, updateBook } = useBooks();
const editing = computed(() => route.meta.mode === 'edit');
const book = ref(null);
const loading = ref(editing.value);
const saving = ref(false);

onMounted(async () => {
  await loadBooks();
  if (editing.value) book.value = state.books.find((item) => item.id === Number(route.params.id)) || null;
  loading.value = false;
  if (editing.value && !book.value) router.replace({ name: 'not-found' });
});

async function save(payload) {
  saving.value = true;
  try {
    if (editing.value) await updateBook(Number(route.params.id), payload);
    else await createBook(payload);
    router.push({ name: 'books' });
  } finally { saving.value = false; }
}
</script>

