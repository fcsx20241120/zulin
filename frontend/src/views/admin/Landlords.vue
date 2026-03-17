<template>
  <div class="landlords">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>房东管理</span>
        </div>
      </template>
      <el-table :data="landlords" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="phone" label="电话" width="150" />
        <el-table-column prop="id_card" label="身份证号" width="200" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
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
import { ElMessage } from 'element-plus'
import { getLandlords, updateLandlord } from '@/api/landlord'

const landlords = ref<any[]>([])
const dialogVisible = ref(false)
const editingId = ref<number | null>(null)
const dialogTitle = ref('编辑房东')
const form = ref<any>({ name: '', phone: '', id_card: '', address: '' })

const loadLandlords = async () => {
  landlords.value = await getLandlords()
}

const handleEdit = (row: any) => {
  editingId.value = row.id
  dialogTitle.value = '编辑房东'
  form.value = {
    name: row.name,
    phone: row.phone,
    id_card: row.id_card,
    address: row.address || ''
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    if (editingId.value) {
      await updateLandlord(editingId.value, form.value)
      ElMessage.success('更新成功')
    }
    
    dialogVisible.value = false
    editingId.value = null
    dialogTitle.value = '编辑房东'
    loadLandlords()
  } catch (error) {
    ElMessage.error('操作失败')
  }
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
