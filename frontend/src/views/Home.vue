<template>
  <div class="home">
    <el-card class="welcome-card">
      <h2>欢迎使用房屋租赁合同管理系统</h2>
      <p>欢迎您，{{ userStore.userInfo?.username || '访客' }}</p>
      <p>当前日期：{{ currentDate }}</p>
    </el-card>

    <el-card class="box-card" style="margin-top: 20px" v-if="expiringLeases.length > 0">
      <template #header>
        <div class="card-header">
          <span>租赁提醒（7 天内到期）</span>
          <el-tag type="danger" v-if="expiringLeases.length > 0">{{ expiringLeases.length }}条</el-tag>
        </div>
      </template>
      <div v-for="item in expiringLeases" :key="item.id" class="lease-item" @click="goToDetail(item.id)">
        <div class="lease-title">{{ item.payment_type }} - ¥{{ item.monthly_rent }}/月</div>
        <div class="lease-info">{{ item.house_address }}</div>
        <div class="lease-info">{{ item.tenant_name }} - {{ item.tenant_phone }}</div>
        <div class="lease-date">到期：{{ formatDate(item.end_date) }}（还剩{{ getDaysRemaining(item.end_date) }}天）</div>
      </div>
    </el-card>

    <el-card class="box-card" style="margin-top: 20px" v-if="overdueLeases.length > 0">
      <template #header>
        <div class="card-header">
          <span>租赁提醒（已超时）</span>
          <el-tag type="danger">{{ overdueLeases.length }}条</el-tag>
        </div>
      </template>
      <div v-for="item in overdueLeases" :key="item.id" class="lease-item overdue" @click="goToDetail(item.id)">
        <div class="lease-title">{{ item.payment_type }} - ¥{{ item.monthly_rent }}/月</div>
        <div class="lease-info">{{ item.house_address }}</div>
        <div class="lease-info">{{ item.tenant_name }} - {{ item.tenant_phone }}</div>
        <div class="lease-date overdue-date">已过期：{{ formatDate(item.end_date) }}（超期{{ getDaysOverdue(item.end_date) }}天）</div>
      </div>
    </el-card>

    <el-card class="box-card" style="margin-top: 20px" v-if="announcements.length > 0">
      <template #header>
        <div class="card-header">
          <span>用户公告</span>
        </div>
      </template>
      <div v-for="item in announcements" :key="item.id" class="announcement-item" @click="showAnnouncementDetail(item)">
        <div class="announcement-title">{{ item.title }}</div>
        <div class="announcement-preview">{{ truncateContent(item.content) }}</div>
        <div class="announcement-date">{{ formatDate(item.created_at) }}</div>
      </div>
    </el-card>

    <el-dialog v-model="detailVisible" :title="selectedAnnouncement?.title" width="600px">
      <div class="announcement-detail">
        <div class="detail-date">{{ selectedAnnouncement ? formatDate(selectedAnnouncement.created_at) : '' }}</div>
        <div class="detail-content">{{ selectedAnnouncement?.content }}</div>
      </div>
      <template #footer>
        <el-button type="primary" @click="detailVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getExpiringLeases, getOverdueLeases } from '@/api/lease'
import { getAnnouncements } from '@/api/announcement'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const currentDate = ref(new Date().toLocaleDateString())
const announcements = ref<any[]>([])
const expiringLeases = ref<any[]>([])
const overdueLeases = ref<any[]>([])
const detailVisible = ref(false)
const selectedAnnouncement = ref<any>(null)

const truncateContent = (content: string): string => {
  if (!content) return ''
  return content.length > 50 ? content.substring(0, 50) + '...' : content
}

const showAnnouncementDetail = (item: any) => {
  selectedAnnouncement.value = item
  detailVisible.value = true
}

const loadAnnouncements = async () => {
  try {
    announcements.value = await getAnnouncements('user')
  } catch (error) {
    console.error('获取公告失败', error)
  }
}

const loadExpiringLeases = async () => {
  if (!userStore.token) {
    return
  }
  try {
    expiringLeases.value = await getExpiringLeases()
  } catch (error) {
    console.error('获取到期合同失败', error)
  }
}

const loadOverdueLeases = async () => {
  if (!userStore.token) {
    return
  }
  try {
    overdueLeases.value = await getOverdueLeases()
  } catch (error) {
    console.error('获取已超时合同失败', error)
  }
}

const goToDetail = (id: number) => {
  router.push(`/lease/${id}`)
}

const formatDate = (date: string | Date): string => {
  if (!date) return ''
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const getDaysRemaining = (endDate: string | Date): number => {
  if (!endDate) return 0
  const end = new Date(endDate)
  const now = new Date()
  const diff = end.getTime() - now.getTime()
  return Math.ceil(diff / (1000 * 60 * 60 * 24))
}

const getDaysOverdue = (endDate: string | Date): number => {
  if (!endDate) return 0
  const end = new Date(endDate)
  const now = new Date()
  const diff = now.getTime() - end.getTime()
  return Math.ceil(diff / (1000 * 60 * 60 * 24))
}

onMounted(() => {
  userStore.getUserInfo()
  loadAnnouncements()
  loadExpiringLeases()
  loadOverdueLeases()
})
</script>

<style scoped>
.home {
  padding: 15px;
  padding-bottom: 70px;
  /* 适配安全区域 */
  padding-top: constant(safe-area-inset-top);
  padding-top: env(safe-area-inset-top);
}

.welcome-card {
  text-align: center;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.announcement-item,
.lease-item {
  padding: 10px 0;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  /* 文字自动换行 */
  word-break: break-word;
}

.announcement-item:last-child,
.lease-item:last-child {
  border-bottom: none;
}

.announcement-item:hover {
  background-color: #f5f7fa;
}

.announcement-title,
.lease-title {
  font-weight: 500;
  /* 防止标题溢出 */
  max-width: 100%;
  overflow-wrap: break-word;
}

.announcement-preview {
  font-size: 13px;
  color: #666;
  margin-top: 5px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.announcement-date,
.lease-date {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
  white-space: nowrap;
}

.announcement-detail {
  padding: 10px 0;
}

.detail-date {
  font-size: 12px;
  color: #999;
  margin-bottom: 15px;
}

.detail-content {
  font-size: 14px;
  line-height: 1.8;
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.lease-info {
  font-size: 13px;
  color: #666;
  margin-top: 4px;
  /* 地址等信息自动换行 */
  word-break: break-word;
}

.lease-item.overdue {
  background-color: #fef0f0;
  padding-left: 10px;
  border-left: 3px solid #f56c6c;
}

.lease-date.overdue-date {
  color: #f56c6c;
  font-weight: 500;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .home {
    padding: 10px;
    padding-bottom: 70px;
  }
  
  .welcome-card h2 {
    font-size: 16px;
  }
  
  .welcome-card p {
    font-size: 13px;
  }
  
  .el-row {
    margin: 0 !important;
  }
  
  .el-col {
    margin-bottom: 15px;
  }
  
  /* 卡片内边距调整 */
  :deep(.el-card__body) {
    padding: 12px;
  }
}

/* 小屏幕手机优化 */
@media (max-width: 480px) {
  .home {
    padding: 8px;
  }
  
  .welcome-card h2 {
    font-size: 15px;
  }
  
  .lease-title {
    font-size: 14px;
  }
  
  .lease-info {
    font-size: 12px;
  }
  
  .announcement-title {
    font-size: 14px;
  }
}

/* 弹窗移动端适配 */
:deep(.el-dialog) {
  max-width: 90%;
  margin: 0 auto;
}

@media (max-width: 480px) {
  :deep(.el-dialog) {
    width: 95% !important;
    max-width: 95% !important;
  }
  
  :deep(.el-dialog__body) {
    max-height: 70vh;
    overflow-y: auto;
  }
}
</style>
