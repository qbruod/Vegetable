<template>
  <div id="app">
    <div class="header">
      <img  src="../pic/shopping-cart.png" alt="my shopping cart">
      <p>My shopping cart</p>
      <el-avatar  src="../pic/pkq.jpg"/>
    </div>
    <!-- <el-steps style="max-width: 600px" :active="active" finish-status="success">
      <el-step title="Step 1"></el-step>
      <el-step>
        <template #title>
          <router-link to="/Photo" class="step-link">Step 2</router-link>
        </template>
      </el-step>
      <el-step>
        <template #title>
          <router-link to="/Buy" class="step-link">Step 3</router-link>
        </template>
      </el-step>
    </el-steps> -->
    <!-- <el-button style="margin-top: 12px" @click="next">Next step</el-button>
    <router-view></router-view> -->

    <el-steps style="max-width: 600px" :active="active" finish-status="success" simple>
      <el-step title="开始拍照" />
      <el-step title="开始结算" />
      <el-step title="完成支付" />
    </el-steps>
    <el-button round  style="margin-top: 12px" @click="next" >Next step</el-button>
    <router-view></router-view>
  </div>

</template>
<style>
body, html {
  margin: 0; /* 确保没有默认的边距 */
  padding: 0;
  background-color: #fcf7f7;
}
.header {
  display: flex; /* 使用Flex布局 */
  align-items: center; /* 垂直居中对齐 */
}
.header img {
  height: 100px;
  width: 100px;
  margin-right: 10px; /* 添加点间距 */
}
.header p {
  flex: 1; /* 让文本区域占据剩余空间 */
  overflow-wrap: break-word; /* 长单词换行 */
}

</style> 
<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router' 
const router = useRouter() 
const active = ref(0)
const next = () => {
  // 根据当前步骤进行跳转
  if (active.value++ > 2) active.value = 0
  // 根据当前步骤进行页面跳转

  if (active.value === 1) {
    router.push('/Photo') // 当active为1时，跳转到/Photo页面
  }
  if (active.value === 2) {
    router.push('/Buy') // 当active为2时，跳转到/Buy页面
  }
  if (active.value === 3) {
    router.push('/Finish') // 当active为3时，跳转到/Finish页面
  }
}
</script>