<template>
  <div class="leases">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>租赁合同列表</span>
          <el-button type="primary" @click="showAddDialog">新增合同</el-button>
        </div>
      </template>
      
      <!-- 桌面端：表格视图 -->
      <el-table :data="leases" style="width: 100%" class="desktop-table">
        <el-table-column prop="house_address" label="房屋地址" min-width="200" />
        <el-table-column label="起租日期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.start_date) }}
          </template>
        </el-table-column>
        <el-table-column label="到期日期" width="120">
          <template #default="{ row }">
            <span :class="['end-date', getDateStatusClass(row.end_date)]">
              {{ formatDate(row.end_date) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="tenant_name" label="租客姓名" width="100" />
        <el-table-column prop="tenant_phone" label="租客电话" width="120" />
        <!-- 状态字段暂时隐藏，保留代码 -->
        <!-- <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'">{{ row.status }}</el-tag>
          </template>
        </el-table-column> -->
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button link type="primary" @click="goToDetail(row.id)">详情</el-button>
            <el-button link type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 移动端：卡片视图 -->
      <div class="mobile-cards">
        <div v-for="item in leases" :key="item.id" class="lease-card">
          <div class="card-header-row">
            <div class="card-title">{{ item.house_address }}</div>
            <!-- 状态字段暂时隐藏，保留代码 -->
            <!-- <el-tag :type="item.status === 'active' ? 'success' : 'info'">{{ item.status }}</el-tag> -->
          </div>
          <div class="card-dates">
            <div class="date-item">
              <span class="date-label">起租</span>
              <span class="date-value">{{ formatDate(item.start_date) }}</span>
            </div>
            <div class="date-item">
              <span class="date-label">到期</span>
              <span :class="['date-value', getDateStatusClass(item.end_date)]">
                {{ formatDate(item.end_date) }}
              </span>
            </div>
          </div>
          <div class="card-info-row">
            <div class="info-item">
              <span class="info-label">租客</span>
              <span class="info-value">{{ item.tenant_name }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">电话</span>
              <span class="info-value">{{ item.tenant_phone }}</span>
            </div>
          </div>
          <div class="card-actions">
            <el-button type="primary" size="small" @click="goToDetail(item.id)">详情</el-button>
            <el-button type="danger" size="small" @click="handleDelete(item.id)">删除</el-button>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 新增合同对话框 - 分步向导 -->
    <el-dialog 
      v-model="dialogVisible" 
      title="新增租赁合同" 
      width="90%"
      :close-on-click-modal="false"
      class="lease-step-dialog"
    >
      <!-- 进度条 -->
      <div class="step-progress">
        <div 
          v-for="(step, index) in steps" 
          :key="index"
          :class="['step-item', { active: currentStep === index, completed: currentStep > index }]"
          @click="canJumpToStep(index) && goToStep(index)"
        >
          <div class="step-circle">
            <span v-if="currentStep > index" class="check-icon">✓</span>
            <span v-else-if="currentStep === index">{{ index + 1 }}</span>
            <span v-else>{{ index + 1 }}</span>
          </div>
          <div class="step-label">{{ step.title }}</div>
        </div>
      </div>

      <!-- 分步表单内容 -->
      <div class="step-content">
        <!-- 步骤 1: 租客信息 -->
        <div v-show="currentStep === 0" class="step-panel">
          <el-form :model="form" label-position="top" ref="tenantFormRef" :rules="tenantRules">
            <el-form-item label="租客姓名" prop="tenant_name" required>
              <el-input v-model="form.tenant_name" placeholder="请输入租客姓名" />
            </el-form-item>
            <el-form-item label="租客身份证号" prop="tenant_id_card">
              <el-input v-model="form.tenant_id_card" placeholder="请输入身份证号" />
            </el-form-item>
            <el-form-item label="租客电话" prop="tenant_phone" required>
              <el-input v-model="form.tenant_phone" placeholder="请输入联系电话" type="tel" />
            </el-form-item>
            <el-form-item label="租客地址" prop="tenant_address">
              <el-input v-model="form.tenant_address" placeholder="请输入地址" />
            </el-form-item>
          </el-form>
        </div>

        <!-- 步骤 2: 房东信息 -->
        <div v-show="currentStep === 1" class="step-panel">
          <el-form :model="form" label-position="top" ref="landlordFormRef" :rules="landlordRules">
            <el-form-item label="房东姓名" prop="landlord_name" required>
              <el-input v-model="form.landlord_name" placeholder="请输入房东姓名" />
            </el-form-item>
            <el-form-item label="房东身份证号" prop="landlord_id_card">
              <el-input v-model="form.landlord_id_card" placeholder="请输入身份证号" />
            </el-form-item>
            <el-form-item label="房东电话" prop="landlord_phone">
              <el-input v-model="form.landlord_phone" placeholder="请输入联系电话" type="tel" />
            </el-form-item>
            <el-form-item label="房东地址" prop="landlord_address">
              <el-input v-model="form.landlord_address" placeholder="请输入地址" />
            </el-form-item>
          </el-form>
        </div>

        <!-- 步骤 3: 房屋信息 -->
        <div v-show="currentStep === 2" class="step-panel">
          <el-form :model="form" label-position="top" ref="houseFormRef" :rules="houseRules">
            <el-form-item label="房屋地址" prop="house_address" required>
              <el-input v-model="form.house_address" placeholder="请输入房屋地址" />
            </el-form-item>
            <el-form-item label="房屋面积" prop="house_area">
              <el-input v-model.number="form.house_area" type="number" placeholder="请输入面积（平方米）" />
            </el-form-item>
            <el-form-item label="房屋用途" prop="house_usage">
              <el-input v-model="form.house_usage" placeholder="请输入房屋用途" />
            </el-form-item>
            <el-form-item label="产权证号" prop="house_property_cert">
              <el-input v-model="form.house_property_cert" placeholder="请输入产权证号" />
            </el-form-item>
          </el-form>
        </div>

        <!-- 步骤 4: 租赁信息 -->
        <div v-show="currentStep === 3" class="step-panel">
          <el-form :model="form" label-position="top" ref="leaseFormRef" :rules="leaseRules">
            <el-form-item label="月租金" prop="monthly_rent" required>
              <el-input v-model.number="form.monthly_rent" type="number" placeholder="请输入月租金额" />
            </el-form-item>
            <el-form-item label="支付方式" prop="payment_type" required>
              <el-select v-model="form.payment_type" style="width: 100%">
                <el-option label="月付" value="月付" />
                <el-option label="季付" value="季付" />
                <el-option label="年付" value="年付" />
              </el-select>
            </el-form-item>
            <el-form-item label="保证金" prop="deposit" required>
              <el-input v-model.number="form.deposit" type="number" placeholder="请输入保证金金额" />
            </el-form-item>
            <el-form-item label="租赁期限" prop="lease_years">
              <el-input v-model.number="form.lease_years" type="number" :min="1" :max="20" placeholder="请输入租期年数" @change="updateEndDate" /> 年
            </el-form-item>
            <el-form-item label="起租日期" prop="start_date" required>
              <el-date-picker 
                v-model="form.start_date" 
                type="date" 
                format="YYYY-MM-DD" 
                value-format="YYYY-MM-DD" 
                style="width: 100%" 
                @change="updateEndDate" 
              />
            </el-form-item>
            <el-form-item label="到期日期" prop="end_date" required>
              <el-date-picker 
                v-model="form.end_date" 
                type="date" 
                format="YYYY-MM-DD" 
                value-format="YYYY-MM-DD" 
                style="width: 100%" 
              />
            </el-form-item>
          </el-form>
        </div>
      </div>

      <!-- 底部按钮 -->
      <template #footer>
        <div class="step-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button v-if="currentStep > 0" @click="prevStep">上一步</el-button>
          <el-button v-if="currentStep < steps.length - 1" type="primary" @click="nextStep">下一步</el-button>
          <el-button v-else type="primary" @click="handleCreate">提交</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { getLeases, createLease, deleteLease } from '@/api/lease'
import { createTenant } from '@/api/tenant'
import { createLandlord } from '@/api/landlord'
import { createHouse } from '@/api/house'
import type { Lease } from '@/api/lease'

const router = useRouter()
const leases = ref<Lease[]>([])
const dialogVisible = ref(false)
const currentStep = ref(0)

const formatDate = (date: Date | string): string => {
  if (!date) return ''
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const getDateStatusClass = (endDate: Date | string): string => {
  if (!endDate) return ''
  const end = new Date(endDate)
  const now = new Date()
  const diffTime = end.getTime() - now.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) {
    return 'overdue'
  } else if (diffDays <= 7) {
    return 'expiring-soon'
  }
  return ''
}

// 步骤定义
const steps = [
  { title: '租客信息' },
  { title: '房东信息' },
  { title: '房屋信息' },
  { title: '租赁信息' }
]

// 表单引用
const tenantFormRef = ref<FormInstance>()
const landlordFormRef = ref<FormInstance>()
const houseFormRef = ref<FormInstance>()
const leaseFormRef = ref<FormInstance>()

// 各步骤校验规则
const tenantRules: FormRules = {
  tenant_name: [{ required: true, message: '请输入租客姓名', trigger: 'blur' }],
  tenant_phone: [
    { required: true, message: '请输入租客电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
}

const landlordRules: FormRules = {
  landlord_name: [{ required: true, message: '请输入房东姓名', trigger: 'blur' }],
  landlord_phone: [
    { required: true, message: '请输入房东电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
}

const houseRules: FormRules = {
  house_address: [{ required: true, message: '请输入房屋地址', trigger: 'blur' }]
}

const leaseRules: FormRules = {
  monthly_rent: [{ required: true, message: '请输入月租金', trigger: 'blur' }],
  payment_type: [{ required: true, message: '请选择支付方式', trigger: 'change' }],
  deposit: [{ required: true, message: '请输入保证金', trigger: 'blur' }],
  start_date: [{ required: true, message: '请选择起租日期', trigger: 'change' }],
  end_date: [{ required: true, message: '请选择到期日期', trigger: 'change' }]
}

const form = ref<Partial<Lease> & {
  tenant_name?: string
  tenant_id_card?: string
  tenant_phone?: string
  tenant_address?: string
  landlord_name?: string
  landlord_id_card?: string
  landlord_phone?: string
  landlord_address?: string
  house_address?: string
  house_area?: number
  house_usage?: string
  house_property_cert?: string
}>({
  tenant_name: '',
  tenant_id_card: '',
  tenant_phone: '',
  tenant_address: '',
  landlord_name: '',
  landlord_id_card: '',
  landlord_phone: '',
  landlord_address: '',
  house_address: '',
  house_area: undefined,
  house_usage: '',
  house_property_cert: '',
  monthly_rent: 1000,
  payment_type: '月付',
  deposit: 1000,
  lease_years: 1,
  start_date: formatDate(new Date()),
  end_date: formatDate(new Date(new Date().setFullYear(new Date().getFullYear() + 1)))
})

const updateEndDate = () => {
  if (form.value.start_date && form.value.lease_years) {
    const startDate = new Date(form.value.start_date)
    const endDate = new Date(startDate)
    endDate.setFullYear(endDate.getFullYear() + form.value.lease_years)
    form.value.end_date = formatDate(endDate)
  }
}

// 分步导航方法
const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const nextStep = async () => {
  const stepRefs = [tenantFormRef, landlordFormRef, houseFormRef, leaseFormRef]
  const currentRef = stepRefs[currentStep.value]
  
  if (!currentRef?.value) {
    currentStep.value++
    return
  }
  
  try {
    await currentRef.value.validate()
    currentStep.value++
  } catch (error) {
    ElMessage.error('请填写完当前步骤的必填项')
  }
}

const goToStep = (step: number) => {
  // 只能跳转到已访问过的步骤或下一步
  if (step <= currentStep.value) {
    currentStep.value = step
  }
}

const canJumpToStep = (step: number): boolean => {
  // 允许点击已完成的步骤
  return step <= currentStep.value
}

const resetForm = () => {
  currentStep.value = 0
  form.value = {
    tenant_name: '',
    tenant_id_card: '',
    tenant_phone: '',
    tenant_address: '',
    landlord_name: '',
    landlord_id_card: '',
    landlord_phone: '',
    landlord_address: '',
    house_address: '',
    house_area: undefined,
    house_usage: '',
    house_property_cert: '',
    monthly_rent: 1000,
    payment_type: '月付',
    deposit: 1000,
    lease_years: 1,
    start_date: formatDate(new Date()),
    end_date: formatDate(new Date(new Date().setFullYear(new Date().getFullYear() + 1)))
  }
  // 重置所有表单校验状态
  tenantFormRef.value?.resetFields()
  landlordFormRef.value?.resetFields()
  houseFormRef.value?.resetFields()
  leaseFormRef.value?.resetFields()
}

const loadLeases = async () => {
  try {
    leases.value = await getLeases()
  } catch (error) {
    console.error('获取租赁合同列表失败', error)
  }
}

const showAddDialog = () => {
  resetForm()
  dialogVisible.value = true
}

const handleCreate = async () => {
  try {
    // 最后一步校验
    if (leaseFormRef.value) {
      await leaseFormRef.value.validate()
    }
    
    // 验证必填字段
    if (!form.value.tenant_name || !form.value.landlord_name || !form.value.house_address) {
      ElMessage.error('请填写租客姓名、房东姓名和房屋地址')
      return
    }
    if (!form.value.monthly_rent || !form.value.deposit) {
      ElMessage.error('请填写月租金和保证金')
      return
    }
    if (!form.value.start_date || !form.value.end_date) {
      ElMessage.error('请选择起租日期和到期日期')
      return
    }

    // 1. 创建租客
    const tenantData = {
      name: form.value.tenant_name,
      id_card: form.value.tenant_id_card || null,
      phone: form.value.tenant_phone || null,
      address: form.value.tenant_address || null
    }
    const tenant: any = await createTenant(tenantData)

    // 2. 创建房东
    const landlordData = {
      name: form.value.landlord_name,
      id_card: form.value.landlord_id_card || null,
      phone: form.value.landlord_phone || null,
      address: form.value.landlord_address || null
    }
    const landlord: any = await createLandlord(landlordData)

    // 3. 创建房屋
    const houseData = {
      address: form.value.house_address,
      area: form.value.house_area || null,
      usage: form.value.house_usage || null,
      property_cert: form.value.house_property_cert || null
    }
    const house: any = await createHouse(houseData)

    // 4. 创建租赁合同
    const leaseData = {
      tenant_id: tenant.id,
      landlord_id: landlord.id,
      house_id: house.id,
      lease_years: form.value.lease_years || 1,
      start_date: form.value.start_date,
      end_date: form.value.end_date,
      monthly_rent: form.value.monthly_rent,
      payment_type: form.value.payment_type,
      deposit: form.value.deposit
    }
    await createLease(leaseData)

    ElMessage.success('创建成功')
    dialogVisible.value = false
    resetForm()
    loadLeases()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '创建失败')
  }
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该合同吗？', '提示', { type: 'warning' })
    await deleteLease(id)
    ElMessage.success('删除成功')
    loadLeases()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

const goToDetail = (id: number) => {
  router.push(`/lease/${id}`)
}

onMounted(() => {
  loadLeases()
})
</script>

<style scoped>
.leases {
  padding: 15px;
  padding-bottom: 70px;
  /* 适配安全区域 */
  padding-top: constant(safe-area-inset-top);
  padding-top: env(safe-area-inset-top);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

/* 桌面端表格 */
.desktop-table {
  display: block;
}

/* 移动端卡片视图 - 默认隐藏 */
.mobile-cards {
  display: none;
}

.end-date {
  padding: 2px 6px;
  border-radius: 4px;
}

.end-date.expiring-soon {
  background-color: #f0f9eb;
  color: #67c23a;
}

.end-date.overdue {
  background-color: #fef0f0;
  color: #f56c6c;
}

/* 移动端卡片样式 */
.lease-card {
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.lease-card:last-child {
  margin-bottom: 0;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  flex: 1;
  margin-right: 10px;
  word-break: break-word;
  line-height: 1.4;
}

.card-dates {
  display: flex;
  gap: 15px;
  margin-bottom: 12px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 6px;
}

.date-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.date-label {
  font-size: 12px;
  color: #909399;
}

.date-value {
  font-size: 13px;
  color: #606266;
  font-weight: 500;
}

.date-value.expiring-soon {
  color: #67c23a;
}

.date-value.overdue {
  color: #f56c6c;
}

.card-info-row {
  display: flex;
  gap: 15px;
  margin-bottom: 12px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.info-label {
  font-size: 12px;
  color: #909399;
}

.info-value {
  font-size: 13px;
  color: #606266;
}

.card-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  padding-top: 12px;
  border-top: 1px solid #e4e7ed;
}

.card-actions .el-button {
  margin: 0;
}

/* 分步对话框样式 */
.lease-step-dialog :deep(.el-dialog__body) {
  padding: 20px 15px;
}

.lease-step-dialog :deep(.el-dialog__footer) {
  padding: 10px 15px;
  border-top: 1px solid #eee;
}

/* 进度条 */
.step-progress {
  display: flex;
  justify-content: space-between;
  margin-bottom: 25px;
  position: relative;
}

.step-progress::before {
  content: '';
  position: absolute;
  top: 15px;
  left: 0;
  right: 0;
  height: 2px;
  background: #e5e5e5;
  z-index: 0;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  cursor: pointer;
  z-index: 1;
  transition: all 0.3s;
}

.step-item.active .step-circle {
  border-color: #409eff;
  background: #409eff;
  color: #fff;
}

.step-item.active .step-label {
  color: #409eff;
  font-weight: 500;
}

.step-item.completed .step-circle {
  border-color: #67c23a;
  background: #67c23a;
  color: #fff;
}

.step-item.completed .step-circle:hover {
  background: #85ce61;
}

.step-circle {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid #e5e5e5;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
}

.step-circle:hover {
  border-color: #409eff;
}

.check-icon {
  color: #fff;
  font-size: 16px;
}

.step-label {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
  transition: all 0.3s;
}

/* 步骤内容 */
.step-content {
  min-height: 300px;
}

.step-panel {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.step-panel :deep(.el-form-item) {
  margin-bottom: 18px;
}

.step-panel :deep(.el-form-item__label) {
  font-weight: 500;
  color: #333;
}

/* 底部按钮 */
.step-footer {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.step-footer .el-button {
  min-width: 80px;
}

/* 表格移动端适配 */
:deep(.el-table) {
  font-size: 13px;
}

:deep(.el-table th) {
  padding: 10px 0;
  font-size: 13px;
}

:deep(.el-table td) {
  padding: 10px 0;
}

/* 响应式：小屏幕显示卡片视图 */
@media (max-width: 768px) {
  .leases {
    padding: 10px;
    padding-bottom: 70px;
  }
  
  /* 隐藏表格，显示卡片 */
  .desktop-table {
    display: none;
  }
  
  .mobile-cards {
    display: block;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .card-header .el-button {
    width: 100%;
  }
}

/* 小屏幕手机优化 */
@media (max-width: 480px) {
  .leases {
    padding: 8px;
  }
  
  .lease-card {
    padding: 12px;
  }
  
  .card-title {
    font-size: 14px;
  }
  
  .card-dates {
    flex-direction: column;
    gap: 10px;
  }
  
  .card-info-row {
    flex-direction: column;
    gap: 10px;
  }
  
  .card-actions {
    flex-direction: column;
    padding-left: 0;
    padding-right: 0;
  }
  
  .card-actions .el-button {
    width: 100%;
    margin: 0 !important;
    box-sizing: border-box;
  }
  
  .step-circle {
    width: 26px;
    height: 26px;
    font-size: 12px;
  }
  
  .step-label {
    font-size: 10px;
  }
  
  .step-footer {
    gap: 6px;
  }
  
  .step-footer .el-button {
    flex: 1;
    min-width: auto;
    padding: 10px 15px;
  }
}

/* 全屏对话框适配移动端 */
@media (max-width: 480px) {
  .lease-step-dialog :deep(.el-dialog) {
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    border-radius: 0;
    height: 100vh;
    max-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .lease-step-dialog :deep(.el-dialog__header) {
    padding: 15px;
    flex-shrink: 0;
  }

  .lease-step-dialog :deep(.el-dialog__body) {
    flex: 1;
    overflow-y: auto;
    padding: 15px;
  }

  .lease-step-dialog :deep(.el-dialog__footer) {
    padding: 15px;
    flex-shrink: 0;
  }

  .step-progress {
    margin-bottom: 20px;
  }

  .step-content {
    min-height: auto;
  }
}

/* 适配 iPhone X 底部安全区域 */
@media (max-width: 480px) and (min-height: 812px) {
  .lease-step-dialog :deep(.el-dialog__footer) {
    padding-bottom: calc(15px + env(safe-area-inset-bottom));
  }
  
  .step-footer {
    padding-bottom: env(safe-area-inset-bottom);
  }
}
</style>
