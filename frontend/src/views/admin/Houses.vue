<template>
  <div class="houses">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>房屋管理</span>
        </div>
      </template>
      <el-table :data="houses" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="address" label="地址" />
        <el-table-column prop="area" label="面积 (㎡)" width="100" />
        <el-table-column prop="usage" label="用途" width="100" />
        <el-table-column prop="property_cert" label="产权证号" width="150" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="地址">
          <el-input v-model="form.address" />
        </el-form-item>
        <el-form-item label="面积">
          <el-input-number v-model="form.area" :min="0" />
        </el-form-item>
        <el-form-item label="用途">
          <el-select v-model="form.usage">
            <el-option label="住宅" value="住宅" />
            <el-option label="商业" value="商业" />
            <el-option label="办公" value="办公" />
          </el-select>
        </el-form-item>
        <el-form-item label="产权证号">
          <el-input v-model="form.property_cert" />
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
import { getHouses, updateHouse } from '@/api/house'

const houses = ref<any[]>([])
const dialogVisible = ref(false)
const editingId = ref<number | null>(null)
const dialogTitle = ref('新增房屋')
const form = ref<any>({ address: '', area: 0, usage: '住宅', property_cert: '' })

const loadHouses = async () => {
  houses.value = await getHouses()
}

const handleEdit = (row: any) => {
  editingId.value = row.id
  dialogTitle.value = '编辑房屋'
  form.value = {
    address: row.address,
    area: row.area,
    usage: row.usage,
    property_cert: row.property_cert || ''
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    if (editingId.value) {
      await updateHouse(editingId.value, form.value)
      ElMessage.success('更新成功')
    }
    
    dialogVisible.value = false
    editingId.value = null
    dialogTitle.value = '编辑房屋'
    loadHouses()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  loadHouses()
})
</script>

<style scoped>
.houses {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
