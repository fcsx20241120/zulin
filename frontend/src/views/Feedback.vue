<template>
  <div class="feedback-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户反馈</span>
          <el-button type="primary" @click="showFeedbackDialog">我要反馈</el-button>
        </div>
      </template>

      <div v-if="feedbacks.length === 0" class="empty-state">
        <el-empty description="暂无反馈记录">
          <el-button type="primary" @click="showFeedbackDialog">提交反馈</el-button>
        </el-empty>
      </div>

      <div v-else class="feedback-list">
        <div v-for="item in feedbacks" :key="item.id" class="feedback-item">
          <div class="feedback-header">
            <div class="feedback-meta">
              <span class="feedback-date">{{ formatDate(item.created_at) }}</span>
              <el-tag :type="getStatusType(item.status)" size="small">
                {{ getStatusText(item.status) }}
              </el-tag>
            </div>
          </div>
          <div class="feedback-content">
            <div class="content-label">我的反馈：</div>
            <div class="content-text">{{ item.content }}</div>
          </div>
          <div v-if="item.reply" class="feedback-reply">
            <div class="content-label">管理员回复：</div>
            <div class="content-text">{{ item.reply }}</div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 提交反馈对话框 -->
    <el-dialog v-model="dialogVisible" title="提交反馈" width="600px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="反馈内容" required>
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="6"
            placeholder="请输入您的意见或建议，我们会认真听取并改进..."
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { createFeedback, getMyFeedbacks, type Feedback } from '@/api/feedback'

const feedbacks = ref<Feedback[]>([])
const dialogVisible = ref(false)
const form = ref({
  content: ''
})

const loadFeedbacks = async () => {
  try {
    feedbacks.value = await getMyFeedbacks()
  } catch (error) {
    console.error('获取反馈列表失败', error)
  }
}

const showFeedbackDialog = () => {
  form.value.content = ''
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!form.value.content.trim()) {
    ElMessage.warning('请输入反馈内容')
    return
  }

  try {
    await createFeedback(form.value.content)
    ElMessage.success('反馈提交成功，我们会尽快处理')
    dialogVisible.value = false
    loadFeedbacks()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '提交失败')
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

onMounted(() => {
  loadFeedbacks()
})
</script>

<style scoped>
.feedback-page {
  padding: 15px;
  padding-bottom: 70px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.empty-state {
  padding: 40px 0;
}

.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.feedback-item {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 15px;
  background: #fff;
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.feedback-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.feedback-date {
  font-size: 13px;
  color: #909399;
}

.feedback-content,
.feedback-reply {
  margin-bottom: 10px;
}

.feedback-reply {
  background: #f5f7fa;
  padding: 12px;
  border-radius: 6px;
  margin-top: 10px;
}

.content-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 6px;
}

.content-text {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  word-break: break-word;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .feedback-page {
    padding: 10px;
  }

  .feedback-item {
    padding: 12px;
  }

  .content-text {
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .feedback-page {
    padding: 8px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .card-header .el-button {
    width: 100%;
  }
}
</style>
