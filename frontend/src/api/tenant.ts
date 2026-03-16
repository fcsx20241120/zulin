import request from './request'

export interface Tenant {
  id: number
  name: string
  address: string | null
  id_card: string | null
  phone: string | null
  created_at: string
}

// 获取租客列表
export function getTenants(skip = 0, limit = 100) {
  return request.get<Tenant[]>('/tenants/', { params: { skip, limit } })
}

// 获取租客详情
export function getTenant(id: number) {
  return request.get<Tenant>(`/tenants/${id}`)
}

// 创建租客
export function createTenant(data: Partial<Tenant>) {
  return request.post('/tenants/', data)
}

// 更新租客
export function updateTenant(id: number, data: Partial<Tenant>) {
  return request.put(`/tenants/${id}`, data)
}

// 删除租客
export function deleteTenant(id: number) {
  return request.delete(`/tenants/${id}`)
}
