<template>
  <div class="lease-detail">
    <el-page-header @back="goBack" :title="`合同详情 #${leaseId}`" />
    
    <el-tabs v-model="activeTab" style="margin-top: 20px">
      <el-tab-pane label="租赁信息" name="lease">
        <el-card v-if="lease">
          <div class="card-actions">
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
                  <div style="display: flex; align-items: center">
                    <el-input-number v-model="leaseForm.lease_years" :min="1" :max="99" style="width: 100%" />
                    <span style="margin-left: 8px; white-space: nowrap">年</span>
                  </div>
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
            <!-- 状态字段暂时隐藏，保留代码 -->
            <!-- <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="状态">
                  <el-tag :type="leaseForm.status === 'active' ? 'success' : 'info'">{{ leaseForm.status }}</el-tag>
                </el-form-item>
              </el-col>
            </el-row> -->
          </el-form>
        </el-card>
      </el-tab-pane>
      <el-tab-pane label="租客信息" name="tenant">
        <el-card>
          <div class="card-actions">
            <el-button type="primary" @click="enableEditTenant" v-if="!isEditingTenant">编辑</el-button>
            <template v-else>
              <el-button type="success" @click="saveTenant">保存</el-button>
              <el-button @click="cancelEditTenant">取消</el-button>
            </template>
          </div>
          <el-form :model="tenantForm" label-width="100px" :disabled="!isEditingTenant" :rules="tenantRules" ref="tenantFormRef">
            <el-form-item label="租客姓名" prop="name">
              <el-input v-model="tenantForm.name" />
            </el-form-item>
            <el-form-item label="租客电话" prop="phone" required>
              <el-input v-model="tenantForm.phone" placeholder="请输入联系电话" />
            </el-form-item>
            <el-form-item label="租客身份证号" prop="id_card">
              <el-input v-model="tenantForm.id_card" />
            </el-form-item>
            <el-form-item label="租客地址" prop="address">
              <el-input v-model="tenantForm.address" />
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
      <el-tab-pane label="房屋信息" name="house">
        <el-card>
          <div class="card-actions">
            <el-button type="primary" @click="enableEditHouse" v-if="!isEditingHouse">编辑</el-button>
            <template v-else>
              <el-button type="success" @click="saveHouse">保存</el-button>
              <el-button @click="cancelEditHouse">取消</el-button>
            </template>
          </div>
          <el-form :model="houseForm" label-width="100px" :disabled="!isEditingHouse">
            <el-form-item label="房屋地址">
              <el-input v-model="houseForm.address" />
            </el-form-item>
            <el-form-item label="房屋面积">
              <div style="display: flex; align-items: center">
                <el-input-number v-model="houseForm.area" :precision="2" :min="0" style="width: 100%" />
                <span style="margin-left: 8px; white-space: nowrap">㎡</span>
              </div>
            </el-form-item>
            <el-form-item label="房屋用途">
              <el-select v-model="houseForm.usage" style="width: 100%">
                <el-option label="住宅" value="住宅" />
                <el-option label="商业" value="商业" />
                <el-option label="办公" value="办公" />
              </el-select>
            </el-form-item>
            <el-form-item label="产权证号">
              <el-input v-model="houseForm.property_cert" />
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
      <el-tab-pane label="房东信息" name="landlord">
        <el-card>
          <div class="card-actions">
            <el-button type="primary" @click="enableEditLandlord" v-if="!isEditingLandlord">编辑</el-button>
            <template v-else>
              <el-button type="success" @click="saveLandlord">保存</el-button>
              <el-button @click="cancelEditLandlord">取消</el-button>
            </template>
          </div>
          <el-form :model="landlordForm" label-width="100px" :disabled="!isEditingLandlord">
            <el-form-item label="房东姓名">
              <el-input v-model="landlordForm.name" />
            </el-form-item>
            <el-form-item label="房东电话">
              <el-input v-model="landlordForm.phone" />
            </el-form-item>
            <el-form-item label="房东身份证号">
              <el-input v-model="landlordForm.id_card" />
            </el-form-item>
            <el-form-item label="房东地址">
              <el-input v-model="landlordForm.address" />
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getLease, updateLease, type Lease } from '@/api/lease'
import { updateTenant, type TenantResponse } from '@/api/tenant'
import { updateHouse, type HouseResponse } from '@/api/house'
import { updateLandlord, type LandlordResponse } from '@/api/landlord'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const leaseId = route.params.id as string
const lease = ref<Lease | null>(null)
const activeTab = ref('lease')
const isEditing = ref(false)
const isEditingTenant = ref(false)
const isEditingHouse = ref(false)
const isEditingLandlord = ref(false)

const leaseForm = ref({
  monthly_rent: 0,
  payment_type: '',
  deposit: 0,
  lease_years: 1,
  start_date: '',
  end_date: '',
  status: ''
})

const tenantForm = ref({
  name: '',
  phone: '',
  id_card: '',
  address: ''
})

const tenantRules = ref({
  name: [{ required: true, message: '请输入租客姓名', trigger: 'blur' }],
  phone: [
    { required: true, message: '请输入租客电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
})

const houseForm = ref({
  address: '',
  area: 0,
  usage: '',
  property_cert: ''
})

const landlordForm = ref({
  name: '',
  phone: '',
  id_card: '',
  address: ''
})

const landlordRules = ref({
  name: [{ required: true, message: '请输入房东姓名', trigger: 'blur' }],
  phone: [
    { required: true, message: '请输入房东电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
})

// 表单引用
const tenantFormRef = ref(null)
const houseFormRef = ref(null)
const landlordFormRef = ref(null)

// 获取租客、房东、房屋 ID（从 lease 中获取）
const tenantId = ref<number | null>(null)
const houseId = ref<number | null>(null)
const landlordId = ref<number | null>(null)

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
      
      // 填充租客信息
      tenantForm.value = {
        name: lease.value.tenant_name || '',
        phone: lease.value.tenant_phone || '',
        id_card: lease.value.tenant_id_card || '',
        address: lease.value.tenant_address || ''
      }
      tenantId.value = lease.value.tenant_id || null
      
      // 填充房屋信息
      houseForm.value = {
        address: lease.value.house_address || '',
        area: lease.value.house_area || 0,
        usage: lease.value.house_usage || '',
        property_cert: lease.value.house_property_cert || ''
      }
      houseId.value = lease.value.house_id || null
      
      // 填充房东信息
      landlordForm.value = {
        name: lease.value.landlord_name || '',
        phone: lease.value.landlord_phone || '',
        id_card: lease.value.landlord_id_card || '',
        address: lease.value.landlord_address || ''
      }
      landlordId.value = lease.value.landlord_id || null
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

// 租客信息编辑方法
const enableEditTenant = () => {
  isEditingTenant.value = true
}

const cancelEditTenant = () => {
  isEditingTenant.value = false
  if (lease.value) {
    tenantForm.value = {
      name: lease.value.tenant_name || '',
      phone: lease.value.tenant_phone || '',
      id_card: lease.value.tenant_id_card || '',
      address: lease.value.tenant_address || ''
    }
  }
}

const saveTenant = async () => {
  try {
    // 表单验证
    if (!tenantFormRef.value) {
      await updateTenant(tenantId.value, tenantForm.value)
      ElMessage.success('保存成功')
      isEditingTenant.value = false
      loadLease()
      return
    }
    
    const valid = await tenantFormRef.value.validate()
    if (!valid) return
    
    if (!tenantId.value) {
      ElMessage.error('租客 ID 不存在')
      return
    }
    await updateTenant(tenantId.value, tenantForm.value)
    ElMessage.success('保存成功')
    isEditingTenant.value = false
    loadLease()
  } catch (error) {
    console.error('保存失败', error)
    ElMessage.error('保存失败')
  }
}

// 房屋信息编辑方法
const enableEditHouse = () => {
  isEditingHouse.value = true
}

const cancelEditHouse = () => {
  isEditingHouse.value = false
  if (lease.value) {
    houseForm.value = {
      address: lease.value.house_address || '',
      area: lease.value.house_area || 0,
      usage: lease.value.house_usage || '',
      property_cert: lease.value.house_property_cert || ''
    }
  }
}

const saveHouse = async () => {
  try {
    if (!houseId.value) {
      ElMessage.error('房屋 ID 不存在')
      return
    }
    await updateHouse(houseId.value, houseForm.value)
    ElMessage.success('保存成功')
    isEditingHouse.value = false
    loadLease()
  } catch (error) {
    console.error('保存失败', error)
    ElMessage.error('保存失败')
  }
}

// 房东信息编辑方法
const enableEditLandlord = () => {
  isEditingLandlord.value = true
}

const cancelEditLandlord = () => {
  isEditingLandlord.value = false
  if (lease.value) {
    landlordForm.value = {
      name: lease.value.landlord_name || '',
      phone: lease.value.landlord_phone || '',
      id_card: lease.value.landlord_id_card || '',
      address: lease.value.landlord_address || ''
    }
  }
}

const saveLandlord = async () => {
  try {
    if (!landlordId.value) {
      ElMessage.error('房东 ID 不存在')
      return
    }
    await updateLandlord(landlordId.value, landlordForm.value)
    ElMessage.success('保存成功')
    isEditingLandlord.value = false
    loadLease()
  } catch (error) {
    console.error('保存失败', error)
    ElMessage.error('保存失败')
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
  /* 适配安全区域 */
  padding-top: constant(safe-area-inset-top);
  padding-top: env(safe-area-inset-top);
}

.card-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 15px;
  flex-wrap: wrap;
  gap: 8px;
}

/* 确保按钮宽度一致且对齐 */
.card-actions .el-button {
  min-width: 64px;
  padding: 12px 20px;
  margin-left: 0;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .lease-detail {
    padding: 10px;
  }
  
  /* 表单在小屏幕上改为竖向布局 */
  :deep(.el-form-item__label) {
    font-size: 13px;
  }
  
  /* 描述列表适配 */
  :deep(.el-descriptions) {
    font-size: 13px;
  }
  
  :deep(.el-descriptions__label) {
    font-size: 12px;
  }
  
  /* 按钮竖向排列 */
  .card-actions {
    flex-direction: column;
    padding-left: 0;
    padding-right: 0;
  }
  
  .card-actions .el-button {
    width: 100%;
    min-width: auto;
    padding: 12px 20px;
    margin-left: 0 !important;
    box-sizing: border-box;
  }
  
  /* 表单字段在小屏幕时每行一个 - 强制覆盖 el-col 的 span 属性 */
  :deep(.el-row .el-col) {
    width: 100% !important;
    max-width: 100% !important;
    flex: 0 0 100% !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
  }
  
  :deep(.el-row) {
    margin-left: 0 !important;
    margin-right: 0 !important;
    display: block !important;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 15px;
  }
  
  /* 确保输入组件宽度 100% */
  :deep(.el-input),
  :deep(.el-input-number),
  :deep(.el-select),
  :deep(.el-date-editor) {
    width: 100% !important;
    max-width: 100% !important;
  }
  
  :deep(.el-input__inner),
  :deep(.el-textarea__inner) {
    font-size: 14px;
    box-sizing: border-box;
  }
}

/* 小屏幕优化 */
@media (max-width: 480px) {
  .lease-detail {
    padding: 8px;
  }
  
  :deep(.el-tabs__item) {
    font-size: 13px;
    padding: 0 12px;
  }
  
  :deep(.el-form-item__label) {
    font-size: 12px;
  }
  
  /* 确保小屏幕每行一个字段 */
  :deep(.el-col) {
    width: 100% !important;
    max-width: 100% !important;
    flex: 0 0 100% !important;
  }
  
  /* 输入组件在小屏幕上也要全宽 */
  :deep(.el-input),
  :deep(.el-input-number),
  :deep(.el-select),
  :deep(.el-date-editor) {
    width: 100% !important;
    max-width: 100% !important;
  }
}

/* 适配 iPhone X 底部安全区域 */
@supports (padding-bottom: env(safe-area-inset-bottom)) {
  .lease-detail {
    padding-bottom: calc(70px + env(safe-area-inset-bottom));
  }
}
</style>
