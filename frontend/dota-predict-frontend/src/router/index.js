/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'
import { isAuthenticated } from "../utils/auth.js"
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import Menu from "../pages/Menu.vue"
import DraftPrediction from "../pages/DraftPrediction.vue"


const routes = [
  // public pages
  { path: '/login', component: Login },
  { path: '/register', component: Register },

  // Common pages
  {
    path: '/menu',
    component: Menu,
    beforeEnter: (to, from, next) => {
      if (isAuthenticated()) next()
      else next('/login')
    },
  },
  {
    path: `/draftPrediction/:matchId`,
    component: DraftPrediction,
    beforeEnter: (to, from, next) => {
      if (isAuthenticated()) next()
      else next('/login')
    },
  },

  // Default redirection
  { path: '/:pathMatch(.*)*', redirect: '/menu' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
