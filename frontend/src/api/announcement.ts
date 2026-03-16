import request from './request'

export interface Announcement {
  id: number
  title: string
  content: string
  type: string
  is_published: boolean
  created_at: string
}

// 获取公告列表
export function getAnnouncements(type?: string) {
  return request.get<Announcement[]>('/announcements/', { params: { type } })
}

// 创建公告
export function createAnnouncement(data: Partial<Announcement>) {
  return request.post('/announcements/', data)
}

// 更新公告
export function updateAnnouncement(id: number, data: Partial<Announcement>) {
  return request.put(`/announcements/${id}`, data)
}

// 删除公告
export function deleteAnnouncement(id: number) {
  return request.delete(`/announcements/${id}`)
}
