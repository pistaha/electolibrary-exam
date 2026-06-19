import { computed, reactive } from 'vue';
import { booksApi } from '@/services/api';

const state = reactive({ books: [], loading: false, error: '', loaded: false, toast: '' });
let toastTimer;

function notify(message) {
  state.toast = message;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { state.toast = ''; }, 2800);
}

async function loadBooks(force = false) {
  if (state.loaded && !force) return;
  state.loading = true;
  state.error = '';
  try {
    state.books = await booksApi.list();
    state.loaded = true;
  } catch (error) {
    state.error = error.message;
  } finally {
    state.loading = false;
  }
}

function replaceBook(updated) {
  const index = state.books.findIndex((book) => book.id === updated.id);
  if (index >= 0) state.books[index] = updated;
  else state.books.unshift(updated);
}

async function createBook(payload) {
  const book = await booksApi.create(payload);
  replaceBook(book);
  notify('Книга добавлена в каталог');
  return book;
}

async function updateBook(id, payload) {
  const book = await booksApi.update(id, payload);
  replaceBook(book);
  notify('Изменения сохранены');
  return book;
}

async function deleteBook(id) {
  await booksApi.remove(id);
  state.books = state.books.filter((book) => book.id !== id);
  notify('Книга удалена');
}

async function runAction(id, action, value) {
  const updated = await booksApi[action](id, value);
  replaceBook(updated);
  return updated;
}

export function useBooks() {
  return {
    state,
    total: computed(() => state.books.length),
    available: computed(() => state.books.filter((book) => book.available).length),
    favorites: computed(() => state.books.filter((book) => book.favorite)),
    collections: computed(() => [...new Set(state.books.map((book) => book.collection_name).filter(Boolean))].sort()),
    loadBooks,
    createBook,
    updateBook,
    deleteBook,
    toggleFavorite: (book) => runAction(book.id, 'favorite', !book.favorite),
    toggleReserve: (book) => runAction(book.id, 'reserve', !book.reserved),
    toggleAvailability: (book) => runAction(book.id, 'availability', !book.available),
    setCollection: (book, name) => runAction(book.id, 'collection', name),
    notify,
  };
}

