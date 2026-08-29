// Copyright 2026 Kevin Fisher. All rights reserved.
// SPDX-License-Identifier: AGPL-3.0-only

import { describe, it, expect, vi, beforeEach } from 'vitest'

import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'

import App from '../App.vue'
import TodayView from '../views/TodayView.vue'
import RandomView from '../views/RandomView.vue'
import RoomView from '../views/RoomView.vue'

beforeEach(() => {
  vi.stubGlobal(
    'fetch',
    vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve([]) })),
  )
})

describe('App', () => {
  it('renders the navigation and the current page', async () => {
    const router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', name: 'today', component: TodayView },
        { path: '/random', name: 'random', component: RandomView },
        { path: '/rooms/:id', name: 'room', component: RoomView, props: true },
      ],
    })
    router.push('/')
    await router.isReady()

    const wrapper = mount(App, {
      global: {
        plugins: [createPinia(), router],
        stubs: {
          FontAwesomeIcon: true,
        },
      },
    })

    expect(wrapper.text()).toContain('Today')
    expect(wrapper.text()).toContain('Random')
    expect(wrapper.text()).toContain('Rooms')
  })
})
