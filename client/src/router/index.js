// Copyright 2026 Kevin Fisher. All rights reserved.
// SPDX-License-Identifier: AGPL-3.0-only

import { createRouter, createWebHistory } from 'vue-router'

import InspectionView from '@/views/InspectionView.vue'
import TodayView from '@/views/TodayView.vue'
import RandomView from '@/views/RandomView.vue'
import RoomView from '@/views/RoomView.vue'
import TaskView from '@/views/TaskView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'today', component: TodayView },
    { path: '/random', name: 'random', component: RandomView },
    { path: '/rooms/:id', name: 'room', component: RoomView, props: true },
    { path: '/rooms/:id/inspect', name: 'room-inspect', component: InspectionView, props: true },
    { path: '/rooms/:id/tasks/:taskId', name: 'task', component: TaskView, props: true },
  ],
})

export default router
