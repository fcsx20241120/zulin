import request from './request'

export interface Feedback {
  id: number
  user_id: number
  content: string
  reply: string | null
  status: string
  created_at: string
  updated_at: string | null
  username?: string
}

// 创建反馈
export function createFeedback(content: string) {
  return request.post('/feedbacks/', { content })
}

// 获取我的反馈列表
export function getMyFeedbacks(skip = 0, limit = 50) {
  return request.get<Feedback[]>('/feedbacks/my', { params: { skip, limit } })
}

// 获取所有反馈（管理员）
export function getAllFeedbacks(skip = 0, limit = 50, status?: string) {
  return request.get<Feedback[]>('/feedbacks/', { params: { skip, limit, status } })
}

// 获取反馈详情
export function getFeedback(id: number) {
  return request.get<Feedback>(`/feedbacks/${id}`)
}

// 回复反馈（管理员）
export function replyFeedback(id: number, reply: string, status: string = 'replied') {
  return request.post(`/feedbacks/${id}/reply`, { reply, status })
}

// 删除反馈（管理员）
export function deleteFeedback(id: number) {
  return request.delete(`/feedbacks/${id}`)
}
