import request from './request'

export interface Lease {
  id: number
  tenant_id: number
  landlord_id: number
  house_id: number
  lease_years: number
  start_date: string
  end_date: string
  monthly_rent: number
  payment_type: string
  deposit: number
  status: string
  created_at: string
  // 房屋信息
  house_address?: string
  house_area?: number
  house_usage?: string
  house_property_cert?: string
  // 租客信息
  tenant_name?: string
  tenant_phone?: string
  tenant_id_card?: string
  tenant_address?: string
  // 房东信息
  landlord_name?: string
  landlord_phone?: string
  landlord_id_card?: string
  landlord_address?: string
}

// 获取租赁合同列表
export function getLeases(skip = 0, limit = 100) {
  return request.get<Lease[]>('/leases/', { params: { skip, limit } })
}

// 获取 7 天内到期合同
export function getExpiringLeases() {
  return request.get<Lease[]>('/leases/expiring')
}

// 获取已超时合同
export function getOverdueLeases() {
  return request.get<Lease[]>('/leases/overdue')
}

// 获取租赁合同详情
export function getLease(id: number) {
  return request.get<Lease>(`/leases/${id}`)
}

// 创建租赁合同
export function createLease(data: Partial<Lease>) {
  return request.post('/leases/', data)
}

// 更新租赁合同
export function updateLease(id: number, data: Partial<Lease>) {
  return request.put(`/leases/${id}`, data)
}

// 导出租赁合同
export function exportLease(id: number) {
  return request.post(`/leases/${id}/export`)
}

// 删除租赁合同
export function deleteLease(id: number) {
  return request.delete(`/leases/${id}`)
}

// 获取统计数据
export function getStats() {
  return request.get<{ contracts: number; tenants: number; houses: number; landlords: number }>('/leases/stats')
}
