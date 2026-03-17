<template>
  <div class="feedbacks">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户反馈管理</span>
          <div class="filter-box">
            <el-select v-model="statusFilter" placeholder="状态筛选" clearable @change="loadFeedbacks">
              <el-option label="待处理" value="pending" />
              <el-option label="已回复" value="replied" />
              <el-option label="已关闭" value="closed" />
            </el-select>
          </div>
        </div>
      </template>

      <el-table :data="feedbacks" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户" width="120" />
        <el-table-column prop="content" label="反馈内容" min-width="200">
          <template #default="{ row }">
            <el-popover placement="top" :width="300" trigger="hover">
              <template #reference>
                <div class="content-preview">{{ truncateContent(row.content) }}</div>
              </template>
              <div class="content-full">{{ row.content }}</div>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column prop="reply" label="回复内容" min-width="150">
          <template #default="{ row }">
            <span v-if="row.reply" class="reply-text">{{ truncateContent(row.reply) }}</span>
            <span v-else class="no-reply">未回复</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="提交时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="showReplyDialog(row)">回复</el-button>
            <el-button link type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 回复对话框 -->
    <el-dialog v-model="replyDialogVisible" title="回复反馈" width="600px">
      <div v-if="selectedFeedback" class="feedback-detail">
        <div class="detail-section">
          <div class="section-title">用户信息</div>
          <div class="section-content">
            <p><strong>用户名：</strong>{{ selectedFeedback.username }}</p>
            <p><strong>提交时间：</strong>{{ formatDate(selectedFeedback.created_at) }}</p>
          </div>
        </div>
        <div class="detail-section">
          <div class="section-title">反馈内容</div>
          <div class="section-content content-text">{{ selectedFeedback.content }}</div>
        </div>
        <div class="detail-section" v-if="selectedFeedback.reply">
          <div class="section-title">当前回复</div>
          <div class="section-content content-text">{{ selectedFeedback.reply }}</div>
        </div>
      </div>
      <el-form :model="replyForm" label-width="80px" style="margin-top: 15px">
        <el-form-item label="回复内容" required>
          <el-input
            v-model="replyForm.reply"
            type="textarea"
            :rows="4"
            placeholder="请输入回复内容"
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="replyForm.status" style="width: 100%">
            <el-option label="待处理" value="pending" />
            <el-option label="已回复" value="replied" />
            <el-option label="已关闭" value="closed" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="replyDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitReply">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getAllFeedbacks,
  replyFeedback,
  deleteFeedback,
  type Feedback
} from '@/api/feedback'

const feedbacks = ref<Feedback[]>([])
const statusFilter = ref<string>('')
const replyDialogVisible = ref(false)
const selectedFeedback = ref<Feedback | null>(null)
const replyForm = ref({
  reply: '',
  status: 'replied'
})

const loadFeedbacks = async () => {
  try {
    feedbacks.value = await getAllFeedbacks(0, 100, statusFilter.value || undefined)
  } catch (error) {
    console.error('获取反馈列表失败', error)
  }
}

const truncateContent = (content: string): string => {
  if (!content) return ''
  return content.length > 30 ? content.substring(0, 30) + '...' : content
}

const getStatusType = (status: string): 'info' | 'success' | 'warning' => {
  switch (status) {
    case 'pending':
      return 'info'
    case 'replied':
      return 'success'
    case 'closed':
      return 'warning'
    default:
      return 'info'
  }
}

const getStatusText = (status: string): string => {
  switch (status) {
    case 'pending':
      return '待处理'
    case 'replied':
      return '已回复'
    case 'closed':
      return '已关闭'
    default:
      return status
  }
}

const showReplyDialog = (feedback: Feedback) => {
  selectedFeedback.value = feedback
  replyForm.value = {
    reply: feedback.reply || '',
    status: feedback.status
  }
  replyDialogVisible.value = true
}

const handleSubmitReply = async () => {
  if (!replyForm.value.reply.trim()) {
    ElMessage.warning('请输入回复内容')
    return
  }

  try {
    if (!selectedFeedback.value) return
    await replyFeedback(
      selectedFeedback.value.id,
      replyForm.value.reply,
      replyForm.value.status
    )
    ElMessage.success('回复成功')
    replyDialogVisible.value = false
    loadFeedbacks()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '回复失败')
  }
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定删除该反馈吗？', '提示', { type: 'warning' })
    await deleteFeedback(id)
    ElMessage.success('删除成功')
    loadFeedbacks()
  } catch (error) {
    // 用户取消删除
  }
}

const formatDate = (date: string | Date): string => {
  if (!date) return ''
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hour = String(d.getHours()).padStart(2, '0')
  const minute = String(d.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day} ${hour}:${minute}`
}

onMounted(() => {
  loadFeedbacks()
})
</script>

<style scoped>
.feedbacks {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-box {
  display: flex;
  gap: 10px;
}

.content-preview {
  cursor: pointer;
  color: #409eff;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 180px;
}

.content-full {
  line-height: 1.6;
  word-break: break-word;
}

.reply-text {
  color: #67c23a;
}

.no-reply {
  color: #909399;
}

.feedback-detail {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 6px;
}

.detail-section {
  margin-bottom: 15px;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #606266;
  margin-bottom: 8px;
}

.section-content {
  font-size: 13px;
  color: #909399;
  line-height: 1.6;
}

.section-content p {
  margin: 4px 0;
}

.content-text {
  background: #fff;
  padding: 10px;
  border-radius: 4px;
  color: #606266;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .feedbacks {
    padding: 10px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .filter-box {
    width: 100%;
  }

  .filter-box .el-select {
    width: 100%;
  }
}
</style>
