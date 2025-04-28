<script lang="ts" setup>
import { ref, onMounted, onUnmounted, toRaw } from 'vue'; // 导入 Vue 方法
import axios from 'axios';
import router from '../router/index.js'; // 确保正确导入 router
import { ElMessageBox, ElMessage } from 'element-plus'; // 导入 Element Plus 的消息和弹框组件
import { CameraFilled, Wallet } from '@element-plus/icons-vue'; // 导入图标

// 拍照预测部分
const video = ref(null);
const canvas = ref(null);
const isCapturing = ref(false);
const isCooldown = ref(false); // 冷却状态
let mediaStream = null;

//购物车全部数据
const tableData = ref([]);
//购物车选择数据
const selectedRows = ref([]);
const totalSubtotal = ref(0);

onMounted(async () => {
  // 初始化摄像头
  mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
  video.value.srcObject = mediaStream;
});

const takePhoto = async () => {
  if (isCapturing.value || isCooldown.value) return; // 防止重复调用或冷却期间调用
  isCapturing.value = true;
  isCooldown.value = true; // 开始冷却

  const context = canvas.value.getContext('2d');
  context.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height);

  const dataURL = canvas.value.toDataURL('image/png');
  const blob = await (await fetch(dataURL)).blob(); // 将 dataURL 转换为 Blob
  const formData = new FormData();
  formData.append('photo', blob, 'photo.png'); // 添加文件到 FormData

  try {
    // 上传图片并获取预测结果
    const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (response.status === 200) {
      const result = response.data; // 后端返回 JSON 数据
      console.log('照片上传成功，预测结果:', result);
      alert(`识别结果: ${result.predicted_class}`); // 显示预测结果

      // 创建 cartItems 数组，从 tableData 中提取所需信息
      const cartItems = tableData.value.map(item => ({
        vegetable_name: item.vegetable_name,
        vegetable_sold: item.quantity, // 假设 quantity 表示已售数量
      }));
      console.log('购物车数据:', cartItems);
      // 使用 axios 发送 POST 请求
      axios.post('http://127.0.0.1:5000/allocate_inventory', {
        predicted_classes: Array.isArray(result.predicted_class)
          ? result.predicted_class // 如果已经是数组，直接使用
          : [result.predicted_class], // 如果不是数组，包装为数组
      })
      .then(res => {
        console.log('库存分配成功:', res.data);
        // 合并新的购物车数据到 tableData
        tableData.value = tableData.value.concat(res.data.cart); // 合并数组
        console.log('购物车数据:', tableData.value);
      })
      .catch(error => {
        console.error('库存分配失败:', error.response ? error.response.data : error.message);
        alert('库存分配失败，请稍后重试或联系管理员');
      });
    } else {
      console.error('照片上传失败');
      alert('照片上传失败，请重试');
    }
  } catch (error) {
    console.error('上传过程中出错:', error);
    alert('上传过程中出错，请检查网络连接');
  } finally {
    // 清空 canvas 并重置状态
    const context = canvas.value.getContext('2d');
    context.clearRect(0, 0, canvas.value.width, canvas.value.height);
    isCapturing.value = false; // 允许下一次拍照

    // 设置冷却时间
    setTimeout(() => {
      isCooldown.value = false; // 冷却结束
    }, 500); // 冷却时间为 0.5 秒
  }
};

onUnmounted(() => {
  if (mediaStream) {
    mediaStream.getTracks().forEach((track) => track.stop());
  }
});

// 购物车部分
const handleSelectionChange = (selection) => {
  selectedRows.value = selection;
  totalSubtotal.value = selectedRows.value.reduce((sum, row) => sum + row.subtotal, 0);
};

const handlePayClick = () => {
  ElMessageBox.confirm('确定要支付吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(() => {
      ElMessage({
        type: 'success',
        message: '支付成功!',
      });

      // 获取原始数组并提取所需字段
      const rawSelectedRows = toRaw(selectedRows.value).map(row => ({
        quantity: row.quantity,
        vegetable_name: row.vegetable_name,
        vegetable_price: row.vegetable_price,
        vegetable_sold: row.vegetable_sold,
      }));
      console.log('支付成功，购物车数据:', rawSelectedRows);

      // 调用保存购物数据接口
      axios.post('http://127.0.0.1:5000/save_vegetables', rawSelectedRows)
        .then(response => {
          console.log('保存成功:', response.data);
        })
        .catch(error => {
          console.error('保存失败:', error.response ? error.response.data : error.message);
        });
      router.push('/Finish'); // 跳转到完成支付页面
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '已取消支付',
      });
    });
};

// 添加图片加载检测
const handleImageLoad = (event: Event) => {
  (event.target as HTMLElement).classList.add('loaded');
};
</script>

<template>
  <div class="photo-page">
    <!-- 左侧拍照区域 -->
    <div class="camera-section">
      <div class="video-wrapper">
        <video ref="video" class="live-feed" autoplay></video>
        <canvas ref="canvas" class="capture-canvas"></canvas>
      </div>
      <el-button 
        type="primary" 
        :icon="CameraFilled" 
        class="capture-button"
        @click="takePhoto" 
        :loading="isCapturing"
        round
      >
        {{ isCapturing ? '识别中...' : '拍照识别' }}
      </el-button>
    </div>

    <!-- 右侧购物车区域 -->
    <div class="cart-section">
      <el-table
        :data="tableData"
        style="width: 100%"
        class="fresh-table"
        @selection-change="handleSelectionChange"
        v-if="tableData.length > 0"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column label="商品图片" width="120">
          <template #default="{ row }">
            <div class="image-wrapper">
              <img 
                :src="`/pic/${row.vegetable_name}.png`" 
                :alt="row.vegetable_name"
                class="product-image"
                loading="lazy"
                @load="handleImageLoad"
              />
            </div>
          </template>
        </el-table-column>
        <el-table-column 
          prop="vegetable_name" 
          label="商品名称" 
          width="180"
        />
        <el-table-column 
          prop="vegetable_price" 
          label="单价（元）" 
          width="120"
        >
          <template #default="{ row }">
            {{ row.vegetable_price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column 
          prop="quantity" 
          label="数量" 
          width="120"
        />
        <el-table-column 
          prop="subtotal" 
          label="小计（元）"
        >
          <template #default="{ row }">
            {{ (row.quantity * row.vegetable_price).toFixed(2) }}
          </template>
        </el-table-column>
      </el-table>

      <!-- 空状态提示 -->
      <div v-if="tableData.length === 0" class="empty-cart">
        <el-empty description="暂未识别到商品，请先拍照添加">
        </el-empty>
      </div>

      <!-- 结算栏 -->
      <div class="checkout-bar">
        <div class="total-info">
          <span class="total-label">已选 {{ selectedRows.length }} 件商品</span>
          <span class="total-amount">
            合计：¥{{ totalSubtotal.toFixed(2) }}
          </span>
        </div>
        <el-button 
          type="success" 
          :icon="Wallet" 
          class="checkout-button"
          @click="handlePayClick"
          :disabled="selectedRows.length === 0"
        >
          立即结算
        </el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 保持原有变量 */
:root {
  --primary-green: #2f855a;
  --fresh-green: #38a169;
  --leaf-green: #9ae6b4;
  --snow-white: #f7fafc;
  --table-hover: #f0fff4;
  --bg-green: #ecf8f1;
}

.photo-page {
  display: grid;
  grid-template-columns: 1fr 2fr; /* 左侧拍照区域 1fr，右侧购物车区域 2fr */
  gap: 2rem;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  background-color: var(--bg-green); /* 设置背景颜色 */
}

/* 拍照区域 */
.camera-section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 24px rgba(46, 204, 113, 0.15);
}

.video-wrapper {
  position: relative;
  max-width: 100%;
  margin: 0 auto;
}

.live-feed {
  width: 100%;
  height: 480px;
  border-radius: 12px;
  background: #000;
  transform: scaleX(-1); /* 镜像翻转 */
}

.capture-button {
  width: 100%;
  max-width: 240px;
  margin: 1.5rem auto 0;
  font-size: 1.1rem;
  background: var(--primary-green) !important;
  transition: all 0.3s ease;
}

.capture-button:hover {
  background: #38a169 !important;
  transform: translateY(-2px);
}

/* 购物车区域 */
.cart-section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 24px rgba(46, 204, 113, 0.15);
}

.fresh-table {
  --el-table-header-bg-color: var(--snow-white);
  --el-table-row-hover-bg-color: var(--table-hover);
  border-radius: 12px;
  overflow: hidden;
}

.fresh-table :deep(.el-table__row) {
  transition: transform 0.3s ease;
}

.fresh-table :deep(.el-table__row:hover) {
  transform: translateX(8px);
}

/* 图片容器 */
.image-wrapper {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  background: #f5f7fa;
  transition: all 0.3s ease;
}

/* 图片样式 */
.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transition: transform 0.3s ease;
}

/* 悬停效果 */
.image-wrapper:hover .product-image {
  transform: scale(1.1);
}

/* 空状态 */
.empty-cart {
  padding: 4rem 0;
  text-align: center;
}

/* 结算栏 */
.checkout-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2rem;
  padding: 1.5rem;
  background: var(--snow-white);
  border-radius: 12px;
}

.total-info {
  display: flex;
  align-items: baseline;
  gap: 1rem;
}

.total-label {
  color: var(--primary-green);
  font-size: 0.95rem;
}

.total-amount {
  color: #ff7621 !important;
  font-size: 1.5rem;
  font-weight: 700;
}

.checkout-button {
  padding: 0.8rem 2.5rem;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.checkout-button:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(56, 161, 105, 0.3);
}

/* 响应式布局 */
@media (max-width: 768px) {
  .photo-page {
    grid-template-columns: 1fr; /* 在小屏幕下改为单列布局 */
    padding: 1rem;
  }

  .video-wrapper {
    height: auto;
  }

  .live-feed {
    height: 300px;
  }

  .checkout-bar {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }

  .image-wrapper {
    width: 60px;
    height: 60px;
  }
}
</style>
``` 