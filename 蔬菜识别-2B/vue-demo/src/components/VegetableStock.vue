<script setup>
import axios from 'axios'
import { reactive, ref, onMounted } from 'vue'
import { ElMessageBox } from 'element-plus'
import _ from 'lodash';

const vegetable_s = reactive([])

const getVegetable = () => {
  axios.get('http://localhost:5000/vegetable_stock/')
    .then(res => {
      vegetable_s.splice(0, vegetable_s.length)
      vegetable_s.push(...res.data.result)
      console.log('更新数据')
    })
    .catch((error) => {
      ElMessageBox.alert(`获取蔬菜数据失败: ${error.message}`, '错误')
      console.error('获取蔬菜数据时出错', error)
    })
}

// 页面渲染后添加数据
onMounted(() => {
  getVegetable()
})

const vegetable_form = reactive({
  vegetable_inventory: "",
})

const handleClose = (done) => {
  ElMessageBox.confirm('确认关闭？')
    .then(() => {
      done()
    })
    .catch(() => {
      // 取消关闭
    })
}

const submitEditForm = _.throttle((formEl) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      axios.put(`http://localhost:5000/vegetable_stock/${vegetable_form.id}`, vegetable_form)
    .then((res) => {
      edit_dialog_visible.value = false
      getVegetable()
    })
    .catch((error) => {
      ElMessageBox.alert(`提交表单失败: ${error.message}`, '错误')
      console.error('提交表单时出错', error)
    });
      console.log('submit!')
    } else {
      console.log('error submit!')
    }
  })
},2000);


const resetForm = (formEl) => {
  formEl.resetFields()
}

const editFormRef = ref()
const edit_dialog_visible = ref(false)
const handleEdit = (vegetable) => {
  for (let key in vegetable) {
    if (vegetable.hasOwnProperty(key)) {
      vegetable_form[key] = vegetable[key]
    }
  }
  edit_dialog_visible.value = true
}

</script>

<template>
  <div style="padding-top: 3%;">
    <p class="fs-1 fw-bolder" style="text-align: center; color: #0d6efd;">库存管理与售出情况查询&#129488;</p>
    <div class="card-container">
      <ul>
        <li v-if="vegetable_s.length > 0" style="padding:20px" v-for="(vegetable, index) in vegetable_s" :key="index">
          <el-card style="max-width: 480px;">
            <template #header>
              <p class="fs-3 fw-bolder" style="text-align: left; color: #4160C2;">{{ vegetable.vegetable_name }}</p>
            </template>
            <img
              :src="`/assets/${vegetable.vegetable_name}.jpg`"
              style="width: 60%; display: block; margin: 0 auto;"
              alt="蔬菜图片"
            />
            <div class="text item" style="display: flex; align-items: center; justify-content: space-between">
              <span class="fs-5 fw-bolder" style="color: #4160C2;">总卖出</span>
              <span class="fs-3 fw-bolder" style="color: #FF5733;">{{ vegetable.vegetable_sold }}</span>
            </div>
            <div class="text item" style="display: flex; align-items: center; justify-content: space-between">
              <span class="fs-5 fw-bolder" style="color: #4160C2;">总库存</span>
              <span class="fs-3 fw-bolder" style="color: #FF5733;">{{ vegetable.vegetable_inventory }}</span>
            </div>
            <div class="d-grid gap-2">
              <button type="button" class="btn btn-primary" style="align-items: center;" @click="handleEdit(vegetable)">
                修改库存
              </button>
            </div>
          </el-card>
        </li>
      </ul>
    </div>

    <el-dialog
      title="修改蔬菜库存信息"
      v-model="edit_dialog_visible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form
        ref="editFormRef"
        :model="vegetable_form"
        status-icon
        label-width="120px"
        class="demo-ruleForm"
      >
        <el-form-item label="库存" prop="vegetable_inventory"
        :rules="[
        { required: true, message: '此项必填!' },
        { type: 'number', message: '只能填入数字!' },
        { validator: (rule, value, callback) => {
          if (value <= 0) {
            callback(new Error('价格必须大于0!'));
          } else {
            callback();
          }
        }
      }]">
          <el-input v-model.number="vegetable_form.vegetable_inventory"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitEditForm(editFormRef)">提交</el-button>
          <el-button @click="resetForm(editFormRef)">重置</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
