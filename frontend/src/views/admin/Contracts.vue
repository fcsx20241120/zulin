<template>
  <div class="contracts">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>合同管理</span>
          <el-button type="primary" @click="dialogVisible = true">新增合同</el-button>
        </div>
      </template>
      <el-table :data="contracts" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="tenant_id" label="租客 ID" width="100" />
        <el-table-column prop="landlord_id" label="房东 ID" width="100" />
        <el-table-column prop="house_id" label="房屋 ID" width="100" />
        <el-table-column prop="monthly_rent" label="月租金" width="100" />
        <el-table-column label="到期日期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.end_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" title="合同信息" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="租客 ID">
          <el-input-number v-model="form.tenant_id" :min="1" />
        </el-form-item>
        <el-form-item label="房东 ID">
          <el-input-number v-model="form.landlord_id" :min="1" />
        </el-form-item>
        <el-form-item label="房屋 ID">
          <el-input-number v-model="form.house_id" :min="1" />
        </el-form-item>
        <el-form-item label="租期 (年)">
          <el-input-number v-model="form.lease_years" :min="1" @change="handleLeaseYearsChange" />
        </el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker v-model="form.start_date" type="date" placeholder="选择日期" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker v-model="form.end_date" type="date" placeholder="选择日期" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="月租金">
          <el-input-number v-model="form.monthly_rent" :min="0" />
        </el-form-item>
        <el-form-item label="支付方式">
          <el-select v-model="form.payment_type">
            <el-option label="月付" value="月付" />
            <el-option label="季付" value="季付" />
            <el-option label="年付" value="年付" />
          </el-select>
        </el-form-item>
        <el-form-item label="保证金">
          <el-input-number v-model="form.deposit" :min="0" />
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
import { getLeases, createLease, updateLease, deleteLease } from '@/api/lease'

const contracts = ref<any[]>([])
const dialogVisible = ref(false)
const getCurrentDate = () => {
  const now = new Date()
  return now.toISOString().split('T')[0]
}

const getDefaultEndDate = (years: number) => {
  const now = new Date()
  now.setFullYear(now.getFullYear() + years)
  return now.toISOString().split('T')[0]
}

const form = ref<any>({
  tenant_id: 1,
  landlord_id: 1,
  house_id: 1,
  lease_years: 1,
  start_date: getCurrentDate(),
  end_date: getDefaultEndDate(1),
  monthly_rent: 1000,
  payment_type: '月付',
  deposit: 1000
})

const loadContracts = async () => {
  contracts.value = await getLeases()
}

const handleLeaseYearsChange = (value: number) => {
  if (form.value.start_date) {
    form.value.end_date = getDefaultEndDate(value)
  }
}

const handleSubmit = async () => {
  try {
    if (!form.value.start_date || !form.value.end_date) {
      ElMessage.error('请选择开始日期和结束日期')
      return
    }
    await createLease(form.value)
    ElMessage.success('创建成功')
    dialogVisible.value = false
    loadContracts()
  } catch (error: any) {
    ElMessage.error('创建失败：' + (error.response?.data?.detail || error.message))
  }
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定删除吗？', '提示', { type: 'warning' })
    await deleteLease(id)
    ElMessage.success('删除成功')
    loadContracts()
  } catch (error) {}
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
  loadContracts()
})
</script>

<style scoped>
.contracts {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
