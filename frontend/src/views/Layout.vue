<template>
  <el-container class="layout-container">
    <el-main class="main-content">
      <router-view />
    </el-main>
    
    <el-footer class="bottom-nav">
      <el-menu 
        mode="horizontal" 
        :default-active="activeMenu" 
        router 
        class="nav-menu"
        :ellipsis="false"
      >
        <el-menu-item index="/home" class="nav-item">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/leases" class="nav-item">
          <el-icon><Document /></el-icon>
          <span>租赁</span>
        </el-menu-item>
        <el-menu-item index="/profile" class="nav-item">
          <el-icon><User /></el-icon>
          <span>我的</span>
        </el-menu-item>
      </el-menu>
    </el-footer>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const activeMenu = computed(() => route.path)
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 0;
  /* 底部导航栏高度 */
  margin-bottom: 60px;
}

.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: #fff;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
  padding: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
}

.nav-menu {
  display: flex;
  justify-content: space-around;
  border-bottom: none;
  width: 100%;
  /* 覆盖 Element Plus 默认样式 */
  border-right: none !important;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60px !important;
  flex: 1;
  max-width: 120px;
}

.nav-item .el-icon {
  font-size: 20px;
  margin-bottom: 2px;
}

.nav-item span {
  font-size: 12px;
}

/* 强制覆盖 Element Plus 样式 */
:deep(.el-menu--horizontal) {
  border-bottom: none !important;
}

:deep(.el-menu-item) {
  height: 60px !important;
  line-height: 60px !important;
  border-bottom: none !important;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .nav-item {
    max-width: none;
  }
  
  .nav-item .el-icon {
    font-size: 20px;
  }
  
  .nav-item span {
    font-size: 11px;
  }
}

/* 小屏幕手机优化 */
@media (max-width: 480px) {
  .bottom-nav {
    height: 55px;
  }
  
  .main-content {
    margin-bottom: 55px;
  }
  
  .nav-item {
    height: 55px !important;
    line-height: 55px !important;
  }
  
  .nav-item .el-icon {
    font-size: 18px;
    margin-bottom: 1px;
  }
  
  .nav-item span {
    font-size: 10px;
  }
}

/* 超小屏幕优化 */
@media (max-width: 375px) {
  .nav-item span {
    font-size: 9px;
  }
  
  .nav-item .el-icon {
    font-size: 16px;
  }
}
</style>
