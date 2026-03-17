<template>
  <router-view />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (token) {
    try {
      await userStore.getUserInfo()
      const role = userStore.userInfo?.role
      const currentPath = route.path
      
      // 管理员访问前台首页，重定向到管理后台
      if (role === 'admin' && currentPath === '/home') {
        router.replace('/admin/dashboard')
      }
      // 普通用户访问管理后台，重定向到前台首页
      if (role === 'user' && currentPath.startsWith('/admin')) {
        router.replace('/home')
      }
    } catch (error) {
      console.error('获取用户信息失败', error)
    }
  }
})
</script>

<style>
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>
