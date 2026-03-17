import request from './request'

export interface House {
  id: number
  address: string
  area: number | null
  usage: string | null
  property_cert: string | null
  created_at: string
}

export type HouseResponse = House

// 获取房屋列表
export function getHouses(skip = 0, limit = 100) {
  return request.get<House[]>('/houses/', { params: { skip, limit } })
}

// 获取房屋详情
export function getHouse(id: number) {
  return request.get<House>(`/houses/${id}`)
}

// 创建房屋
export function createHouse(data: Partial<House>) {
  return request.post('/houses/', data)
}

// 更新房屋
export function updateHouse(id: number, data: Partial<House>) {
  return request.put(`/houses/${id}`, data)
}

// 删除房屋
export function deleteHouse(id: number) {
  return request.delete(`/houses/${id}`)
}
