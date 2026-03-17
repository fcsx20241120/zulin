<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-title">合同总数</div>
          <div class="stat-value">{{ stats.contracts }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-title">租客总数</div>
          <div class="stat-value">{{ stats.tenants }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-title">房屋总数</div>
          <div class="stat-value">{{ stats.houses }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-title">房东总数</div>
          <div class="stat-value">{{ stats.landlords }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card style="margin-top: 20px">
      <template #header>
        <span>系统公告</span>
      </template>
      <el-empty v-if="announcements.length === 0" description="暂无公告" />
      <div v-for="item in announcements" :key="item.id" class="announcement-item">
        <div class="announcement-title">{{ item.title }}</div>
        <div class="announcement-content">{{ item.content }}</div>
        <div class="announcement-date">{{ formatDate(item.created_at) }}</div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAnnouncements } from '@/api/announcement'
import { getStats } from '@/api/lease'

const stats = ref({
  contracts: 0,
  tenants: 0,
  houses: 0,
  landlords: 0
})

const announcements = ref<any[]>([])

const loadStats = async () => {
  try {
    stats.value = await getStats()
  } catch (error) {
    console.error('获取统计数据失败', error)
  }
}

const loadAnnouncements = async () => {
  try {
    announcements.value = await getAnnouncements('system')
  } catch (error) {
    console.error('获取公告失败', error)
  }
}

const formatDate = (date: string | Date): string => {
  if (!date) return ''
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

onMounted(() => {
  loadStats()
  loadAnnouncements()
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.stat-card {
  text-align: center;
}

.stat-title {
  font-size: 14px;
  color: #999;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
}

.announcement-item {
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.announcement-item:last-child {
  border-bottom: none;
}

.announcement-title {
  font-weight: 500;
  margin-bottom: 5px;
}

.announcement-content {
  color: #666;
  margin-bottom: 5px;
}

.announcement-date {
  font-size: 12px;
  color: #999;
}
</style>
