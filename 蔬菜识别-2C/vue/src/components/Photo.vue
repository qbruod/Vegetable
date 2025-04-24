<template>
    <div>
      <video ref="video" width="400" height="300" autoplay></video>
      <canvas ref="canvas" style="display: none;"></canvas>
      <el-button type="paizhao" round @click="takePhoto" :disabled="isCapturing">拍照</el-button>
      <el-button type="baocun" round @click="savePhoto" :disabled="!hasPhotoToSave">保存</el-button>
      <a ref="downloadLink" href="#" download="photo.png" style="display: none;"></a>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue';
import {paizhao,baocun} from '@element-plus/icons-vue'
const video = ref(null);
const canvas = ref(null);
const downloadLink = ref(null);
const isCapturing = ref(false); 
const hasPhotoToSave = ref(false); 
let mediaStream = null;

onMounted(async () => {
  mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
  video.value.srcObject = mediaStream;
});
// 当Vue组件被挂载后，它会尝试访问用户的摄像头，获取视频流，并立即将这个视频流显示在一个HTML的<video>元素中，实现视频的实时预览功能
const takePhoto = () => {
  hasPhotoToSave.value = true; // 准备好照片供保存
  const context = canvas.value.getContext('2d');
  context.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height);
};

const savePhoto = async () => {
  if (hasPhotoToSave.value) {
    const dataURL = canvas.value.toDataURL('image/png');
    const blob = await (await fetch(dataURL)).blob(); // 将 dataURL 转换为 Blob
    const formData = new FormData();
    formData.append('photo', blob, 'photo.png'); // 添加文件到 FormData

    try {
      // 使用 fetch 将图片上传到后端
      const response = await fetch('http://your-backend-url/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        console.log('照片上传成功');
      } else {
        console.error('照片上传失败');
      }
    } catch (error) {
      console.error('上传过程中出错:', error);
    }

    hasPhotoToSave.value = false; // 保存后重置状态
  }
};

onUnmounted(() => {
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop());
  }
});
</script>
