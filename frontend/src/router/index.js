import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  { path: '/', name: 'home', component: () => import('@/views/HomeView.vue') },
  {
    path: '/books',
    component: () => import('@/views/BooksShellView.vue'),
    children: [
      { path: '', name: 'books', component: () => import('@/views/BooksView.vue') },
      { path: 'new', name: 'book-new', component: () => import('@/views/BookFormView.vue'), meta: { mode: 'create' } },
      { path: ':id/edit', name: 'book-edit', component: () => import('@/views/BookFormView.vue'), meta: { mode: 'edit' } },
    ],
  },
  { path: '/favorites', name: 'favorites', component: () => import('@/views/FavoritesView.vue') },
  { path: '/collections', name: 'collections', component: () => import('@/views/CollectionsView.vue') },
  { path: '/about', name: 'about', component: () => import('@/views/AboutView.vue') },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('@/views/NotFoundView.vue') },
];

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
});

