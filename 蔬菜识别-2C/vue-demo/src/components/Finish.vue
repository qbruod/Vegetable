<template>
  <div class="finish-container">
    <el-row justify="center" align="middle">
      <el-col :xs="24" :sm="20" :md="16" :lg="12">
        <el-result class="success-card">
          <template #icon>
            <div class="animated-checkmark">
              <svg class="checkmark" viewBox="0 0 52 52">
                <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/>
                <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
              </svg>
            </div>
          </template>
          <template #title>
            <h1 class="success-title">支付成功！🎉</h1>
          </template>
          <template #sub-title>
            <div class="success-subtitle">
              <p>感谢您的购买！订单已确认完成</p>
              <p class="order-info">订单编号：#{{ Math.floor(Math.random() * 1000000) }}</p>
            </div>
          </template>
          <template #extra>
            <el-button 
              type="primary" 
              class="return-button"
              @click="router.push('/')"
            >
              🛒 返回购物首页
            </el-button>
          </template>
        </el-result>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();
</script>

<style scoped>
/* 颜色变量 */
:root {
  --success-green: #2ecc71;
  --light-green: #ecf8f1;
  --dark-green: #27ae60;
}

.finish-container {
  min-height: 100vh;
  background: #ecf8f1;

  align-items: center;
  padding: 2rem;
}

.success-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 24px rgba(46, 204, 113, 0.15);
}

/* 动画勾勾样式 */
.animated-checkmark {
  margin: 0 auto 2rem;
  width: 100px;
}

.checkmark__circle {
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  stroke-width: 2;
  stroke-miterlimit: 10;
  stroke: #2ecc71;
  fill: none;
  animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}

.checkmark__check {
  transform-origin: 50% 50%;
  stroke-dasharray: 48;
  stroke-dashoffset: 48;
  stroke: #2ecc71;
  animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
}

@keyframes stroke {
  100% {
    stroke-dashoffset: 0;
  }
}

@keyframes scale {
  0%, 100% {
    transform: none;
  }
  50% {
    transform: scale3d(1.1, 1.1, 1);
  }
}

.success-title {
  color: #27ae60;
  font-size: 2rem;
  margin-bottom: 1rem;
}

.success-subtitle {
  color: #666;
  line-height: 1.6;
  
  p {
    margin: 0.5rem 0;
  }
}

.order-info {
  font-size: 0.9em;
  color: #999;
}

.return-button {
  margin-top: 2rem;
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
  background: #2ecc71 !important;
  border: none;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .success-title {
    font-size: 1.5rem;
  }
  
  .return-button {
    width: 100%;
    padding: 1rem;
  }
}
</style>