<script setup>
import axios from 'axios';
import { reactive, ref, onMounted } from 'vue';
import { ElMessageBox } from 'element-plus';
import _ from 'lodash';

const vegetable_s = reactive([]);
const vegetable_stock_s = reactive([]);

const getVegetable = () => {
  axios.get('http://localhost:5000/vegetable/').then(res => {
    vegetable_s.splice(0, vegetable_s.length);
    vegetable_s.push(...res.data.result);
    console.log('更新数据');
  }).catch(error => {
    ElMessageBox.alert(`获取蔬菜数据失败: ${error.message}`, '错误');
    console.error('获取蔬菜数据时出错', error);
  });
};

const getVegetableStock = () => {
  axios.get('http://localhost:5000/vegetable_stock/').then(res => {
    vegetable_stock_s.splice(0, vegetable_stock_s.length);
    vegetable_stock_s.push(...res.data.result);
    console.log('更新数据');
  }).catch(error => {
    ElMessageBox.alert(`获取蔬菜库存数据失败: ${error.message}`, '错误');
    console.error('获取蔬菜库存数据时出错', error);
  });
};

onMounted(() => {
  getVegetable();
  getVegetableStock();
});

const handleDelete = (index, scope) => {
  console.log(index, scope);
  axios.delete(`http://localhost:5000/vegetable/${scope.id}`).then(() => {
    getVegetable();
  });
};

const add_dialog_visible = ref(false);
const ruleFormRef = ref();
const vegetable_form = reactive({
  vegetable_name: "",
  vegetable_sold: "",
  vegetable_inventory: "",
  vegetable_price: "",
});

const handleClose = (done) => {
  ElMessageBox.confirm('确认关闭？')
    .then(() => {
      done();
    })
    .catch(() => {});
};


const submitForm = _.throttle((formE1) => {
  if (!formE1) return
  formE1.validate((valid) => {
    if (valid) {
      axios.post('http://localhost:5000/vegetable_s', vegetable_form).then(() => {
      add_dialog_visible.value = false;
      formE1.resetFields();
      getVegetable();
    });
      console.log('submit!')
    } else {
      console.log('error submit!')
    }
  })
},2000);//设置一个两秒的节流，不然提交容易混乱

const resetForm = (formE1) => {
  formE1.resetFields();
};

const editFormRef = ref();
const edit_dialog_visible = ref(false);
const handleEdit = (index, scope) => {
  Object.assign(vegetable_form, scope);
  edit_dialog_visible.value = true;
};

const submitEnitForm = _.throttle((formE1) => {
  if (!formE1) return
  formE1.validate((valid) => {
    if (valid) {
      axios.put(`http://localhost:5000/vegetable/${vegetable_form.id}`, vegetable_form).then(() => {
      edit_dialog_visible.value = false;
      getVegetable();
    });
      console.log('submit!')
    } else {
      console.log('error submit!')
    }
  })
},2000);

const findInventory = (vegetableName) => {
  const stockItem = vegetable_stock_s.find(item => item.vegetable_name === vegetableName);
  return stockItem ? stockItem.vegetable_inventory : 0;
};
</script>

<template>
<div style="margin: 0 auto;width:70%;padding-top: 3%;">
  <p class="fs-1 fw-bolder" style="text-align: center;color: #0b5ed7">蔬菜信息管理&#129299;&#9997;</p>
  <button type="button" class="btn btn-primary" @click="add_dialog_visible=true">添加蔬菜售出信息</button>
  <el-table :data="vegetable_s" style="margin:20px auto;">
    <el-table-column label="编号" prop="id" />
    <el-table-column label="卖出时间" prop="time" />
    <el-table-column label="蔬菜名称" prop="vegetable_name" />
    <el-table-column label="售出数量" prop="vegetable_sold" />
    <el-table-column label="库存" prop="vegetable_inventory" />
    <el-table-column label="价格" prop="vegetable_price" />
    <el-table-column align="right" label="操作" width="200px">
      <template #default="scope">
        <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
          编辑
        </el-button>
        <el-button
          size="small"
          type="danger"
          @click="handleDelete(scope.$index, scope.row)">
          删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>

</div>

<el-dialog
  title="添加蔬菜售出信息"
  v-model="add_dialog_visible"
  width="30%"
  :before-close="handleClose"
  v-if="vegetable_stock_s.length > 0"
>
  <el-form 
    ref="ruleFormRef" 
    :model="vegetable_form"
    status-icon
    label-width="120px"
    class="demo-ruleForm">
    <el-form-item label="蔬菜名称" prop="vegetable_name" :rules="[{ required: true, message: '此项必选!' }]">
      <el-select
        v-model="vegetable_form.vegetable_name"
        placeholder="选择蔬菜"
      >
        <el-option v-for="(item, index) in vegetable_stock_s" :key="index" :label="item.vegetable_name" :value="item.vegetable_name" />
      </el-select>
    </el-form-item>
    <el-form-item
      label="售出数量"
      prop="vegetable_sold"
      :rules="[
        { required: true, message: '此项必填!' },
        { type: 'number', message: '只能填入数字!' },
        { validator: (rule, value, callback) => {
          if (value <= 0) {
            callback(new Error('售出数量必须大于0!'));
          } 
          else if(value>findInventory(vegetable_form.vegetable_name)){
            callback(new Error('售出数超出库存数!'));
          }
          else {
            callback();
          }
        }
      }]">
      <el-input v-model.number="vegetable_form.vegetable_sold" type="text"></el-input>
    </el-form-item>
    <el-form-item label="价格" prop="vegetable_price" :rules="[
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
      <el-input v-model.number="vegetable_form.vegetable_price" type="text"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm(ruleFormRef)">提交</el-button>
      <el-button @click="resetForm(ruleFormRef)">重置</el-button>
    </el-form-item>
  </el-form>
</el-dialog>

<!-- 编辑蔬菜信息页面 -->
<el-dialog
  title="修改蔬菜售出信息"
  v-model="edit_dialog_visible"
  width="30%"
  :before-close="handleClose"
  v-if="vegetable_stock_s.length > 0"
>
  <el-form 
    ref="editFormRef" 
    :model="vegetable_form"
    status-icon
    label-width="120px"
    class="demo-ruleForm">
    <el-form-item label="蔬菜名称" prop="vegetable_name">
      <el-input v-model="vegetable_form.vegetable_name" readonly></el-input>
    </el-form-item>
    <el-form-item
      label="售出数量"
      prop="vegetable_sold"
      :rules="[
        { required: true, message: '此项必填!' },
        { type: 'number', message: '只能填入数字!' },
        { validator: (rule, value, callback) => {
          if (value <= 0) {
            callback(new Error('售出数量必须大于0!'));
          } 
          else if(value>findInventory(vegetable_form.vegetable_name)){
            callback(new Error('售出数超出库存数!'));
          }
          else {
            callback();
          }
        }
      }]">
      <el-input v-model.number="vegetable_form.vegetable_sold" type="text"></el-input>
    </el-form-item>
    <el-form-item label="价格" prop="vegetable_price" :rules="[
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
      <el-input v-model.number="vegetable_form.vegetable_price" type="text"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitEnitForm(editFormRef)">提交</el-button>
      <el-button @click="resetForm(editFormRef)">重置</el-button>
    </el-form-item>
  </el-form>
</el-dialog>
</template>
