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
import { UserFilled } from '@element-plus/icons-vue'
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
</script>

<style scoped>
.profile {
  padding: 20px;
  min-height: calc(100vh - 120px);
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
</style>
