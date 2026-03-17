<template>
  <div class="profile">
    <el-card>
      <template #header>
        <span>我的</span>
      </template>
      
      <div v-if="userStore.token" class="logged-in">
        <div class="user-avatar">
          <el-avatar :size="60" :icon="UserFilled" />
        </div>
        <div class="user-name">{{ userStore.userInfo?.username || '用户' }}</div>
        
        <el-descriptions :column="1" border class="user-info">
          <el-descriptions-item label="用户名">{{ userStore.userInfo?.username || '-' }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ userStore.userInfo?.email || '-' }}</el-descriptions-item>
          <el-descriptions-item label="电话">{{ userStore.userInfo?.phone || '-' }}</el-descriptions-item>
          <el-descriptions-item label="角色">
            <el-tag :type="userStore.userInfo?.role === 'admin' ? 'danger' : 'primary'">
              {{ userStore.userInfo?.role === 'admin' ? '管理员' : '普通用户' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
        
        <div class="menu-list">
          <div class="menu-item" @click="goToFeedback">
            <span class="menu-icon">💬</span>
            <span class="menu-text">用户反馈</span>
            <el-icon class="menu-arrow"><ArrowRight /></el-icon>
          </div>
        </div>
        
        <el-button type="danger" class="logout-btn" @click="handleLogout">退出登录</el-button>
      </div>
      
      <div v-else class="not-logged-in">
        <el-empty description="您尚未登录" />
        <el-button type="primary" class="login-btn" @click="goToLogin">去登录</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { UserFilled, ArrowRight } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}

const goToLogin = () => {
  router.push('/login')
}

const goToFeedback = () => {
  router.push('/feedback')
}
</script>

<style scoped>
.profile {
  padding: 20px;
  min-height: calc(100vh - 120px);
  /* 适配安全区域 */
  padding-top: constant(safe-area-inset-top);
  padding-top: env(safe-area-inset-top);
}

.logged-in {
  text-align: center;
}

.user-avatar {
  margin-bottom: 15px;
}

.user-name {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
}

.user-info {
  margin-bottom: 20px;
  text-align: left;
}

.menu-list {
  margin-bottom: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background: #fff;
  cursor: pointer;
  transition: background 0.3s;
  border-bottom: 1px solid #e4e7ed;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-item:hover {
  background: #f5f7fa;
}

.menu-icon {
  font-size: 20px;
  margin-right: 10px;
}

.menu-text {
  flex: 1;
  font-size: 14px;
  color: #606266;
}

.menu-arrow {
  font-size: 16px;
  color: #909399;
}

.logout-btn {
  width: 100%;
  max-width: 200px;
}

.not-logged-in {
  padding: 40px 0;
}

.login-btn {
  width: 100%;
  max-width: 200px;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .profile {
    padding: 15px;
  }
  
  .user-name {
    font-size: 16px;
  }
  
  :deep(.el-descriptions) {
    font-size: 13px;
  }
  
  :deep(.el-descriptions__label) {
    font-size: 12px;
  }
}

/* 小屏幕优化 */
@media (max-width: 480px) {
  .profile {
    padding: 10px;
  }
  
  .user-avatar {
    margin-bottom: 12px;
  }
  
  :deep(.el-avatar) {
    width: 50px !important;
    height: 50px !important;
  }
  
  .user-name {
    font-size: 15px;
  }
}
</style>
