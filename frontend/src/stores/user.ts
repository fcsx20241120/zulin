import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login, register, getCurrentUser, type UserInfo } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  const userInfo = ref<UserInfo | null>(null)

  // 登录
  async function userLogin(username: string, password: string) {
    const res = await login({ username, password })
    token.value = res.access_token
    userInfo.value = res
    localStorage.setItem('token', res.access_token)
    return res
  }

  // 注册
  async function userRegister(username: string, password: string, email?: string, phone?: string) {
    return await register({ username, password, email, phone })
  }

  // 获取用户信息
  async function getUserInfo() {
    const res = await getCurrentUser()
    userInfo.value = res
    return res
  }

  // 登出
  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }

  return {
    token,
    userInfo,
    userLogin,
    userRegister,
    getUserInfo,
    logout
  }
})
