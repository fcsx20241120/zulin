<template>
  <div class="houses">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>房屋管理</span>
          <el-button type="primary" @click="dialogVisible = true">新增房屋</el-button>
        </div>
      </template>
      <el-table :data="houses" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="address" label="地址" />
        <el-table-column prop="area" label="面积 (㎡)" width="100" />
        <el-table-column prop="usage" label="用途" width="100" />
        <el-table-column prop="property_cert" label="产权证号" width="150" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" title="房屋信息" width="500px">
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { getHouses, createHouse, updateHouse, deleteHouse } from '@/api/house'

const houses = ref<any[]>([])
const dialogVisible = ref(false)
const form = ref<any>({ address: '', area: 0, usage: '住宅', property_cert: '' })

const loadHouses = async () => {
  houses.value = await getHouses()
}

const handleSubmit = async () => {
  try {
    await createHouse(form.value)
    ElMessage.success('创建成功')
    dialogVisible.value = false
    loadHouses()
  } catch (error) {
    ElMessage.error('创建失败')
  }
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定删除吗？', '提示', { type: 'warning' })
    await deleteHouse(id)
    ElMessage.success('删除成功')
    loadHouses()
  } catch (error) {}
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
