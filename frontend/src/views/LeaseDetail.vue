<template>
  <div class="lease-detail">
    <el-page-header @back="goBack" :title="`合同详情 #${leaseId}`" />
    
    <el-tabs v-model="activeTab" style="margin-top: 20px">
      <el-tab-pane label="租赁信息" name="lease">
        <el-card v-if="lease">
          <div class="card-actions">
            <el-button type="success" @click="exportLease">导出合同</el-button>
            <el-button type="primary" @click="enableEdit" v-if="!isEditing">编辑</el-button>
            <template v-else>
              <el-button type="success" @click="saveLease">保存</el-button>
              <el-button @click="cancelEdit">取消</el-button>
            </template>
          </div>
          <el-form :model="leaseForm" label-width="100px" :disabled="!isEditing">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="月租金">
                  <el-input-number v-model="leaseForm.monthly_rent" :precision="2" :step="100" :min="0" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="支付方式">
                  <el-select v-model="leaseForm.payment_type" placeholder="请选择" style="width: 100%">
                    <el-option label="月付" value="月付" />
                    <el-option label="季付" value="季付" />
                    <el-option label="半年付" value="半年付" />
                    <el-option label="年付" value="年付" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="保证金">
                  <el-input-number v-model="leaseForm.deposit" :precision="2" :step="1000" :min="0" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="租赁期限">
                  <el-input-number v-model="leaseForm.lease_years" :min="1" :max="99" style="width: 100%" />
                  <span style="margin-left: 10px">年</span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="起租日期">
                  <el-date-picker v-model="leaseForm.start_date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="到期日期">
                  <el-date-picker v-model="leaseForm.end_date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" style="width: 100%" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="状态">
                  <el-tag :type="leaseForm.status === 'active' ? 'success' : 'info'">{{ leaseForm.status }}</el-tag>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </el-card>
      </el-tab-pane>
      <el-tab-pane label="租客信息" name="tenant">
        <el-card>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="租客姓名">{{ lease?.tenant_name || '-' }}</el-descriptions-item>
            <el-descriptions-item label="租客电话">{{ lease?.tenant_phone || '-' }}</el-descriptions-item>
            <el-descriptions-item label="租客身份证号" :span="2">{{ lease?.tenant_id_card || '-' }}</el-descriptions-item>
            <el-descriptions-item label="租客地址" :span="2">{{ lease?.tenant_address || '-' }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-tab-pane>
      <el-tab-pane label="房屋信息" name="house">
        <el-card>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="房屋地址" :span="2">{{ lease?.house_address || '-' }}</el-descriptions-item>
            <el-descriptions-item label="房屋面积">{{ lease?.house_area ? lease.house_area + '㎡' : '-' }}</el-descriptions-item>
            <el-descriptions-item label="房屋用途">{{ lease?.house_usage || '-' }}</el-descriptions-item>
            <el-descriptions-item label="产权证号" :span="2">{{ lease?.house_property_cert || '-' }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-tab-pane>
      <el-tab-pane label="房东信息" name="landlord">
        <el-card>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="房东姓名">{{ lease?.landlord_name || '-' }}</el-descriptions-item>
            <el-descriptions-item label="房东电话">{{ lease?.landlord_phone || '-' }}</el-descriptions-item>
            <el-descriptions-item label="房东身份证号" :span="2">{{ lease?.landlord_id_card || '-' }}</el-descriptions-item>
            <el-descriptions-item label="房东地址" :span="2">{{ lease?.landlord_address || '-' }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getLease, updateLease, exportLease as exportLeaseApi, type Lease } from '@/api/lease'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const leaseId = route.params.id as string
const lease = ref<Lease | null>(null)
const activeTab = ref('lease')
const isEditing = ref(false)

const leaseForm = ref({
  monthly_rent: 0,
  payment_type: '',
  deposit: 0,
  lease_years: 1,
  start_date: '',
  end_date: '',
  status: ''
})

const loadLease = async () => {
  try {
    lease.value = await getLease(Number(leaseId))
    if (lease.value) {
      leaseForm.value = {
        monthly_rent: lease.value.monthly_rent,
        payment_type: lease.value.payment_type,
        deposit: lease.value.deposit,
        lease_years: lease.value.lease_years,
        start_date: formatDate(lease.value.start_date),
        end_date: formatDate(lease.value.end_date),
        status: lease.value.status
      }
    }
  } catch (error) {
    console.error('获取合同详情失败', error)
  }
}

const enableEdit = () => {
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
  if (lease.value) {
    leaseForm.value = {
      monthly_rent: lease.value.monthly_rent,
      payment_type: lease.value.payment_type,
      deposit: lease.value.deposit,
      lease_years: lease.value.lease_years,
      start_date: formatDate(lease.value.start_date),
      end_date: formatDate(lease.value.end_date),
      status: lease.value.status
    }
  }
}

const saveLease = async () => {
  try {
    await updateLease(Number(leaseId), leaseForm.value)
    ElMessage.success('保存成功')
    isEditing.value = false
    loadLease()
  } catch (error) {
    console.error('保存失败', error)
    ElMessage.error('保存失败')
  }
}

const exportLease = async () => {
  try {
    const res = await exportLeaseApi(Number(leaseId))
    ElMessage.success(`合同已导出到 out/${res.file_name}`)
  } catch (error) {
    console.error('导出失败', error)
    ElMessage.error('导出失败')
  }
}

const goBack = () => {
  router.back()
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
  loadLease()
})
</script>

<style scoped>
.lease-detail {
  padding: 15px;
  padding-bottom: 70px;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 15px;
}

@media (max-width: 768px) {
  .lease-detail {
    padding: 10px;
  }
}
</style>
