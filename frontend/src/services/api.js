const API = '/api';

async function request(path, options = {}) {
  const response = await fetch(`${API}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (response.status === 204) return null;
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.detail || 'Не удалось выполнить запрос');
  return body;
}

export const booksApi = {
  list: () => request('/books'),
  get: (id) => request(`/books/${id}`),
  create: (book) => request('/books', { method: 'POST', body: JSON.stringify(book) }),
  update: (id, book) => request(`/books/${id}`, { method: 'PUT', body: JSON.stringify(book) }),
  remove: (id) => request(`/books/${id}`, { method: 'DELETE' }),
  favorite: (id, value) => request(`/books/${id}/favorite`, { method: 'PATCH', body: JSON.stringify({ value }) }),
  reserve: (id, value) => request(`/books/${id}/reserve`, { method: 'PATCH', body: JSON.stringify({ value }) }),
  availability: (id, value) => request(`/books/${id}/availability`, { method: 'PATCH', body: JSON.stringify({ value }) }),
  collection: (id, collection_name) => request(`/books/${id}/collection`, { method: 'PATCH', body: JSON.stringify({ collection_name }) }),
};

