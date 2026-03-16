import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue')
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/views/Layout.vue'),
    children: [
      {
        path: '',
        redirect: '/home'
      },
      {
        path: '/home',
        name: 'Home',
        component: () => import('@/views/Home.vue')
      },
      {
        path: '/leases',
        name: 'Leases',
        component: () => import('@/views/Leases.vue')
      },
      {
        path: '/lease/:id',
        name: 'LeaseDetail',
        component: () => import('@/views/LeaseDetail.vue')
      },
      {
        path: '/profile',
        name: 'Profile',
        component: () => import('@/views/Profile.vue')
      }
    ]
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/admin/Layout.vue'),
    children: [
      {
        path: '',
        redirect: '/admin/dashboard'
      },
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue')
      },
      {
        path: 'contracts',
        name: 'AdminContracts',
        component: () => import('@/views/admin/Contracts.vue')
      },
      {
        path: 'tenants',
        name: 'AdminTenants',
        component: () => import('@/views/admin/Tenants.vue')
      },
      {
        path: 'houses',
        name: 'AdminHouses',
        component: () => import('@/views/admin/Houses.vue')
      },
      {
        path: 'landlords',
        name: 'AdminLandlords',
        component: () => import('@/views/admin/Landlords.vue')
      },
      {
        path: 'system',
        name: 'AdminSystem',
        component: () => import('@/views/admin/System.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
