import request from './request'

export interface User {
  id: number
  username: string
  email: string | null
  phone: string | null
  role: string
  is_active: boolean
  created_at: string
  updated_at: string | null
}

// 获取用户列表
export function getUsers() {
  return request.get<User[]>('/users/')
}

// 创建用户
export function createUser(data: { 
  username: string
  password: string
  email?: string
  phone?: string
  role?: string
  is_active?: boolean
}) {
  return request.post('/users/', data)
}

// 更新用户
export function updateUser(id: number, data: Partial<User>) {
  return request.put(`/users/${id}`, data)
}

// 删除用户
export function deleteUser(id: number) {
  return request.delete(`/users/${id}`)
}
