<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const active = ref(0)

const next = () => {
  router.push('/Photo')
  active.value = 1
}
</script>

<template>
  <div id="app">
    <nav class="vegetable-navbar">
      <div class="nav-container">
        <div class="nav-title">
          <h1 class="brand-text">🛒 蔬菜购物车 🛒</h1>
        </div>
      </div>
    </nav>

    <!-- 欢迎界面 -->
    <div v-if="active === 0" class="welcome-container">
      <div class="emoji-wall">
        <span class="spin">🌱</span>
        <span class="bounce">🥬</span>
        <span class="spin reverse">🥕</span>
        <span class="bounce delay">🍅</span>
        <span class="spin">🌽</span>
      </div>
      
      <div class="welcome-card">
        <h2 class="title">欢迎来到智能蔬菜超市！</h2>
        <p class="subtitle">点击下方按钮开始拍照选购 🎉</p>
        
        <el-button 
          type="primary" 
          class="start-button"
          @click="next"
        >
          📸 开始拍照
        </el-button>
      </div>
    </div>

    <router-view></router-view>
  </div>
</template>

<style>
/* 全局颜色定义 */
:root {
  --primary-green: #2ecc71;      /* 鲜绿色 */
  --dark-green: #27ae60;         /* 深绿色 */
  --bg-green: #ecf8f1;           /* 背景浅绿 */
  --text-green: #1d5e3a;         /* 文本深绿 */
}

/* 导航栏垂直居中修正 */
.vegetable-navbar {
  height: 64px;
  background: var(--primary-green) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-container {
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: center; /* 新增水平居中 */
  align-items: center;     /* 确保垂直居中 */
  padding: 0 20px;
}

.brand-text {
  color: white !important;
  font-size: 1.8rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-align: center; /* 水平居中 */
  justify-content: center; /* Flex 水平居中 */
  width: 100%; /* 确保占满父容器宽度 */
}

.nav-title {
  flex-grow: 1;
  text-align: center; /* 新增文本水平居中 */
}

.brand-text {
  color: white;
  font-size: 1.8rem;
  margin: 0;
  padding: 0;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

/* 欢迎界面容器 */
.welcome-container {
  min-height: calc(100vh - 64px);
  background: var(--bg-green);
  padding: 2rem;
  text-align: center;
}

/* Emoji 动画墙 */
.emoji-wall {
  margin: 3rem 0;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.emoji-wall span {
  font-size: 4rem;
  display: inline-block;
}

.spin {
  animation: spin 8s linear infinite;
}

.spin.reverse {
  animation-direction: reverse;
}

.bounce {
  animation: bounce 1.5s ease-in-out infinite;
}

.delay {
  animation-delay: 0.5s;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

/* 欢迎卡片 */
.welcome-card {
  background: white;
  max-width: 600px;
  margin: 0 auto;
  padding: 3rem;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(46, 204, 113, 0.15);
}

.title {
  color: var(--text-green);
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.subtitle {
  color: var(--dark-green);
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

/* 开始按钮 */
.start-button {
  background: var(--primary-green) !important;
  border: none;
  padding: 1rem 2.5rem !important;
  font-size: 1.2rem !important;
  border-radius: 50px !important;
  transition: all 0.3s ease;
}

.start-button:hover {
  background: var(--dark-green) !important;
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(46, 204, 113, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .brand-text {
    font-size: 1.4rem;
  }
  
  .emoji-wall {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .welcome-card {
    padding: 2rem;
  }
  
  .title {
    font-size: 2rem;
  }
}

</style>