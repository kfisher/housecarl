import { createRouter, createWebHistory } from 'vue-router'

import TodayView from '@/views/TodayView.vue'
import RandomView from '@/views/RandomView.vue'
import RoomView from '@/views/RoomView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'today', component: TodayView },
    { path: '/random', name: 'random', component: RandomView },
    { path: '/rooms/:id', name: 'room', component: RoomView, props: true },
  ],
})

export default router
