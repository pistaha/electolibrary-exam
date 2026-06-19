<template>
  <form class="book-form" novalidate @submit.prevent="submit">
    <div class="form-grid">
      <label class="field span-2">
        <span>Название *</span>
        <input v-model.trim="form.title" type="text" placeholder="Например, Чапаев и Пустота" @blur="touched.title = true" />
        <small v-if="touched.title && errors.title" class="error">{{ errors.title }}</small>
      </label>
      <label class="field">
        <span>Автор *</span>
        <input v-model.trim="form.author" type="text" placeholder="Имя и фамилия" @blur="touched.author = true" />
        <small v-if="touched.author && errors.author" class="error">{{ errors.author }}</small>
      </label>
      <label class="field">
        <span>Издательство *</span>
        <select v-model="form.publisher">
          <option value="" disabled>Выберите издательство</option>
          <option v-for="publisher in publishers" :key="publisher">{{ publisher }}</option>
        </select>
      </label>
      <label class="field span-2">
        <span>Описание *</span>
        <textarea v-model.trim="form.description" rows="5" placeholder="Краткая аннотация книги" @blur="touched.description = true" />
        <small v-if="touched.description && errors.description" class="error">{{ errors.description }}</small>
      </label>
      <label class="field">
        <span>Год издания *</span>
        <input v-model.number="form.publication_year" type="number" min="1450" :max="currentYear" />
      </label>
      <label class="field">
        <span>Подборка</span>
        <input v-model.trim="form.collection_name" type="text" list="collections" placeholder="Например, Русская классика" />
        <datalist id="collections"><option v-for="item in collections" :key="item" :value="item" /></datalist>
      </label>
      <fieldset class="field span-2 rating-field">
        <legend>Возрастной рейтинг *</legend>
        <label v-for="rating in ratings" :key="rating" :class="['rating-option', { selected: form.age_rating === rating }]">
          <input v-model="form.age_rating" type="radio" :value="rating" />{{ rating }}
        </label>
      </fieldset>
      <label class="field span-2 upload-field">
        <span>Обложка JPG</span>
        <input type="file" accept="image/jpeg,.jpg,.jpeg" @change="readCover" />
        <small>До 1,5 МБ. Файл сохраняется вместе с записью книги.</small>
      </label>
      <div v-if="form.cover_url" class="cover-preview span-2">
        <img :src="form.cover_url" alt="Предпросмотр обложки" />
        <button class="text-button" type="button" @click="form.cover_url = ''">Удалить обложку</button>
      </div>
      <label class="checkbox-field span-2"><input v-model="form.available" type="checkbox" /> Книга доступна для выдачи</label>
    </div>
    <p v-if="fileError" class="form-alert">{{ fileError }}</p>
    <div class="form-actions">
      <button class="button button-primary" type="submit" :disabled="saving">{{ saving ? 'Сохраняем…' : submitLabel }}</button>
      <button class="button button-light" type="button" @click="$emit('cancel')">Отмена</button>
    </div>
  </form>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue';

const props = defineProps({
  initial: { type: Object, default: null },
  saving: { type: Boolean, default: false },
  submitLabel: { type: String, default: 'Сохранить книгу' },
  collections: { type: Array, default: () => [] },
});
const emit = defineEmits(['submit', 'cancel']);
const currentYear = new Date().getFullYear();
const ratings = ['0+', '6+', '12+', '16+', '18+'];
const publishers = ['АСТ', 'Эксмо', 'Вагриус', 'ЛитРес Классика', 'Питер', 'Манн, Иванов и Фербер', 'Prentice Hall', 'O’Reilly Media'];
const form = reactive(emptyForm());
const touched = reactive({ title: false, author: false, description: false });
const fileError = ref('');

function emptyForm() {
  return {
    title: '', author: '', description: '', cover_url: '', publisher: '',
    publication_year: currentYear, age_rating: '12+', available: true,
    favorite: false, reserved: false, collection_name: '',
  };
}

watch(() => props.initial, (value) => Object.assign(form, emptyForm(), value || {}), { immediate: true });

const errors = computed(() => ({
  title: form.title.length >= 2 ? '' : 'Введите минимум 2 символа',
  author: form.author.length >= 2 ? '' : 'Укажите автора',
  description: form.description.length >= 10 ? '' : 'Описание должно содержать минимум 10 символов',
  publisher: form.publisher ? '' : 'Выберите издательство',
  year: form.publication_year >= 1450 && form.publication_year <= currentYear ? '' : `Год должен быть от 1450 до ${currentYear}`,
}));

function readCover(event) {
  fileError.value = '';
  const [file] = event.target.files;
  if (!file) return;
  if (file.type !== 'image/jpeg') { fileError.value = 'Выберите файл в формате JPG'; return; }
  if (file.size > 1_500_000) { fileError.value = 'Размер обложки не должен превышать 1,5 МБ'; return; }
  const reader = new FileReader();
  reader.onload = () => { form.cover_url = reader.result; };
  reader.readAsDataURL(file);
}

function submit() {
  Object.keys(touched).forEach((key) => { touched[key] = true; });
  if (Object.values(errors.value).some(Boolean)) return;
  emit('submit', { ...form });
}
</script>
