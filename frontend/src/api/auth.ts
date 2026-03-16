import request from './request'

export interface LoginParams {
  username: string
  password: string
}

export interface RegisterParams {
  username: string
  password: string
  email?: string
  phone?: string
}

export interface UserInfo {
  id: number
  username: string
  email: string | null
  phone: string | null
  role: string
}

// 登录
export function login(data: LoginParams) {
  const formData = new FormData()
  formData.append('username', data.username)
  formData.append('password', data.password)
  return request.post('/auth/login', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  })
}

// 注册
export function register(data: RegisterParams) {
  return request.post('/auth/register', data)
}

// 获取当前用户信息
export function getCurrentUser() {
  return request.get('/auth/me')
}
