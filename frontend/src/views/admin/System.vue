<template>
  <div class="system">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="公告管理" name="announcement">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>公告列表</span>
              <el-button type="primary" @click="showAnnouncementDialog">新增公告</el-button>
            </div>
          </template>
          <el-table :data="announcements" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="title" label="标题" />
            <el-table-column prop="type" label="类型" width="100">
              <template #default="{ row }">
                <el-tag :type="row.type === 'system' ? 'danger' : 'primary'">
                  {{ row.type === 'system' ? '系统公告' : '用户公告' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="is_published" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.is_published ? 'success' : 'info'">
                  {{ row.is_published ? '已发布' : '未发布' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button link type="primary" @click="editAnnouncement(row)">编辑</el-button>
                <el-button link type="danger" @click="handleDeleteAnnouncement(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
      <el-tab-pane label="用户管理" name="user">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>用户列表</span>
              <el-button type="primary" @click="showUserDialog">新增用户</el-button>
            </div>
          </template>
          <el-table :data="users" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="username" label="用户名" />
            <el-table-column prop="email" label="邮箱" width="180" />
            <el-table-column prop="phone" label="电话" width="130" />
            <el-table-column prop="role" label="角色" width="100">
              <template #default="{ row }">
                <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'">
                  {{ row.role === 'admin' ? '管理员' : '普通用户' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="is_active" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'info'">
                  {{ row.is_active ? '正常' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button link type="primary" @click="editUser(row)" :disabled="row.username === 'admin'">编辑</el-button>
                <el-button link type="danger" @click="handleDeleteUser(row.id)" :disabled="row.username === 'admin'">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <el-dialog v-model="announcementDialogVisible" :title="announcementDialogTitle" width="600px">
      <el-form :model="announcementForm" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="announcementForm.title" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="announcementForm.type">
            <el-option label="用户公告" value="user" />
            <el-option label="系统公告" value="system" />
          </el-select>
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="announcementForm.content" type="textarea" :rows="5" />
        </el-form-item>
        <el-form-item label="发布">
          <el-switch v-model="announcementForm.is_published" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="announcementDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitAnnouncement">确定</el-button>
      </template>
    </el-dialog>
    
    <!-- 用户管理对话框 -->
    <el-dialog v-model="userDialogVisible" :title="userDialogTitle" width="500px">
      <el-form :model="userForm" label-width="80px">
        <el-form-item label="用户名" required>
          <el-input v-model="userForm.username" :disabled="!!editingUserId" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" :required="!editingUserId">
          <el-input v-model="userForm.password" type="password" :placeholder="editingUserId ? '不修改请留空' : '请输入密码'" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="userForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="userForm.phone" placeholder="请输入电话" />
        </el-form-item>
        <el-form-item label="角色" required>
          <el-select v-model="userForm.role" style="width: 100%">
            <el-option label="普通用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="userForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="userDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitUserForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAnnouncements, createAnnouncement, updateAnnouncement, deleteAnnouncement } from '@/api/announcement'
import { getUsers, createUser, updateUser, deleteUser } from '@/api/user'

const activeTab = ref('announcement')
const announcements = ref<any[]>([])
const users = ref<any[]>([])

// 公告相关
const announcementDialogVisible = ref(false)
const editingAnnouncementId = ref<number | null>(null)
const announcementDialogTitle = ref('编辑公告')
const announcementForm = ref<any>({ title: '', content: '', type: 'user', is_published: true })

// 用户相关
const userDialogVisible = ref(false)
const editingUserId = ref<number | null>(null)
const userDialogTitle = ref('新增用户')
const userForm = ref<any>({ 
  username: '', 
  password: '', 
  email: '', 
  phone: '', 
  role: 'user',
  is_active: true 
})

const loadAnnouncements = async () => {
  announcements.value = await getAnnouncements()
}

const showAnnouncementDialog = () => {
  editingAnnouncementId.value = null
  announcementDialogTitle.value = '新增公告'
  announcementForm.value = { title: '', content: '', type: 'user', is_published: true }
  announcementDialogVisible.value = true
}

const editAnnouncement = (row: any) => {
  editingAnnouncementId.value = row.id
  announcementDialogTitle.value = '编辑公告'
  announcementForm.value = {
    title: row.title,
    content: row.content,
    type: row.type,
    is_published: row.is_published
  }
  announcementDialogVisible.value = true
}

const submitAnnouncement = async () => {
  try {
    if (editingAnnouncementId.value) {
      // 编辑模式
      await updateAnnouncement(editingAnnouncementId.value, announcementForm.value)
      ElMessage.success('更新成功')
    } else {
      // 新增模式
      await createAnnouncement(announcementForm.value)
      ElMessage.success('创建成功')
    }
    
    announcementDialogVisible.value = false
    editingAnnouncementId.value = null
    announcementDialogTitle.value = '编辑公告'
    loadAnnouncements()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleDeleteAnnouncement = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定删除吗？', '提示', { type: 'warning' })
    await deleteAnnouncement(id)
    ElMessage.success('删除成功')
    loadAnnouncements()
  } catch (error) {
    // 用户取消删除
  }
}

onMounted(() => {
  loadAnnouncements()
  loadUsers()
})

const loadUsers = async () => {
  try {
    users.value = await getUsers()
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  }
}

const showUserDialog = () => {
  editingUserId.value = null
  userDialogTitle.value = '新增用户'
  userForm.value = { 
    username: '', 
    password: '', 
    email: '', 
    phone: '', 
    role: 'user',
    is_active: true 
  }
  userDialogVisible.value = true
}

const editUser = (row: any) => {
  editingUserId.value = row.id
  userDialogTitle.value = '编辑用户'
  userForm.value = {
    username: row.username,
    password: '',
    email: row.email || '',
    phone: row.phone || '',
    role: row.role,
    is_active: row.is_active
  }
  userDialogVisible.value = true
}

const submitUserForm = async () => {
  try {
    if (!userForm.value.username) {
      ElMessage.error('请输入用户名')
      return
    }
    
    if (!editingUserId.value && !userForm.value.password) {
      ElMessage.error('请输入密码')
      return
    }
    
    const formData = { ...userForm.value }
    if (editingUserId.value && !formData.password) {
      delete formData.password
    }
    
    if (editingUserId.value) {
      // 编辑模式
      await updateUser(editingUserId.value, formData)
      ElMessage.success('更新成功')
    } else {
      // 新增模式
      await createUser(formData)
      ElMessage.success('创建成功')
    }
    
    userDialogVisible.value = false
    editingUserId.value = null
    userDialogTitle.value = '新增用户'
    loadUsers()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  }
}

const handleDeleteUser = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定删除该用户吗？', '提示', { 
      type: 'warning',
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    })
    await deleteUser(id)
    ElMessage.success('删除成功')
    loadUsers()
  } catch (error) {
    // 用户取消删除
  }
}
</script>

<style scoped>
.system {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
