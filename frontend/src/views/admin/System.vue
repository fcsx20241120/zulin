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
                <el-button link type="danger" @click="deleteAnnouncement(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
      <el-tab-pane label="用户管理" name="user">
        <el-card>
          <template #header>
            <span>用户列表</span>
          </template>
          <el-table :data="users" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="username" label="用户名" />
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
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <el-dialog v-model="announcementDialogVisible" title="公告信息" width="600px">
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAnnouncements, createAnnouncement, updateAnnouncement, deleteAnnouncement } from '@/api/announcement'

const activeTab = ref('announcement')
const announcements = ref<any[]>([])
const users = ref<any[]>([])
const announcementDialogVisible = ref(false)
const announcementForm = ref<any>({ title: '', content: '', type: 'user', is_published: true })

const loadAnnouncements = async () => {
  announcements.value = await getAnnouncements()
}

const showAnnouncementDialog = () => {
  announcementForm.value = { title: '', content: '', type: 'user', is_published: true }
  announcementDialogVisible.value = true
}

const submitAnnouncement = async () => {
  try {
    await createAnnouncement(announcementForm.value)
    ElMessage.success('创建成功')
    announcementDialogVisible.value = false
    loadAnnouncements()
  } catch (error) {
    ElMessage.error('创建失败')
  }
}

const deleteAnnouncement = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定删除吗？', '提示', { type: 'warning' })
    await deleteAnnouncement(id)
    ElMessage.success('删除成功')
    loadAnnouncements()
  } catch (error) {}
}

onMounted(() => {
  loadAnnouncements()
})
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
