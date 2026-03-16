<template>
  <div class="landlords">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>房东管理</span>
          <el-button type="primary" @click="dialogVisible = true">新增房东</el-button>
        </div>
      </template>
      <el-table :data="landlords" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="phone" label="电话" width="150" />
        <el-table-column prop="id_card" label="身份证号" width="200" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" title="房东信息" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="姓名">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="身份证">
          <el-input v-model="form.id_card" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.address" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getLandlords, createLandlord, updateLandlord, deleteLandlord } from '@/api/landlord'

const landlords = ref<any[]>([])
const dialogVisible = ref(false)
const form = ref<any>({ name: '', phone: '', id_card: '', address: '' })

const loadLandlords = async () => {
  landlords.value = await getLandlords()
}

const handleSubmit = async () => {
  try {
    await createLandlord(form.value)
    ElMessage.success('创建成功')
    dialogVisible.value = false
    loadLandlords()
  } catch (error) {
    ElMessage.error('创建失败')
  }
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定删除吗？', '提示', { type: 'warning' })
    await deleteLandlord(id)
    ElMessage.success('删除成功')
    loadLandlords()
  } catch (error) {}
}

onMounted(() => {
  loadLandlords()
})
</script>

<style scoped>
.landlords {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
