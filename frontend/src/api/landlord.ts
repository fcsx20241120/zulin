import request from './request'

export interface Landlord {
  id: number
  name: string
  address: string | null
  id_card: string | null
  phone: string | null
  created_at: string
}

export type LandlordResponse = Landlord

// 获取房东列表
export function getLandlords(skip = 0, limit = 100) {
  return request.get<Landlord[]>('/landlords/', { params: { skip, limit } })
}

// 获取房东详情
export function getLandlord(id: number) {
  return request.get<Landlord>(`/landlords/${id}`)
}

// 创建房东
export function createLandlord(data: Partial<Landlord>) {
  return request.post('/landlords/', data)
}

// 更新房东
export function updateLandlord(id: number, data: Partial<Landlord>) {
  return request.put(`/landlords/${id}`, data)
}

// 删除房东
export function deleteLandlord(id: number) {
  return request.delete(`/landlords/${id}`)
}
