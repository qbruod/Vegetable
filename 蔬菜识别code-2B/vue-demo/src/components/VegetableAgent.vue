<script setup>
import axios from 'axios';
// 引入 Vue 的 reactive、ref 和 onMounted，用于响应式数据和生命周期管理
import { reactive, ref, onMounted, nextTick } from 'vue';
import { ElMessageBox } from 'element-plus';
// 引入 lodash 库，用于工具函数的使用
import _ from 'lodash';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import { computed } from 'vue';

marked.use({
  extensions: [
    {
      name: 'latex',
      level: 'inline',
      start(src) { return src.indexOf('\\(') }, // 匹配 \( 开头
      tokenizer(src) {
        const match = src.match(/^\\\((.*?)\\\)/); // 匹配 \(...\)
        if (match) {
          return {
            type: 'latex',
            raw: match[0],
            text: match[1].trim()
          };
        }
      },
      renderer(token) {
        return `<span class="math-inline">\\(${token.text}\\)</span>`; // 包裹公式
      }
    }
  ]
});

// 引入 MathJax
const MathJax = window.MathJax;

// 定义响应式数据，用于存储逐条消息内容
const messages = ref([]);
const vegetable_s = reactive([]);

// 修改 getVegetable 为返回 Promise
const getVegetable = () => {
  return axios.get('http://localhost:5000/vegetable/')
    .then(res => {
      vegetable_s.splice(0, vegetable_s.length);
      vegetable_s.push(...res.data.result);
      console.log(...res.data.result);
    })
    .catch(error => {
      ElMessageBox.alert(`获取蔬菜数据失败: ${error.message}`, '错误');
      console.error('获取蔬菜数据时出错', error);
    });
};

// 定义函数发送 POST 请求并逐条处理消息
const fetchDataWithTypingEffect = async () => {
  try {
    const content = `分析一下数据库信息，我的数据库信息为${JSON.stringify(vegetable_s)}`;
    console.log('请求内容:', content); // 打印请求内容到控制台

    const response = await axios.post(
      'https://api.coze.cn/v3/chat?conversation_id=7490931536938696744&stream=true',
      {
        bot_id: "7490563331921543194",
        user_id: "user",
        auto_save_history: true,
        stream: false,
        additional_messages: [
          {
            content: content, // 使用拼接后的字符串
            content_type: "text",
            type: "question",
            role: "user"
          }
        ]
      },
      {
        headers: {
          Authorization: 'Bearer pat_r26vcxpAo92sJ5ivwYHAsCzyvz8BsUn35VO9j3XT8dprSvmBVJaCuV3yaCCAluZG',
          'Content-Type': 'application/json'
        }
      }
    );

    console.log('Response:', response.data);
    const conversation_id = response.data.data.conversation_id.toString();
    const chat_id = response.data.data.id.toString();
    console.log('conversation_id:', conversation_id);
    console.log('chat_id:', chat_id);

    // 显示“正在查询”的字样
    messages.value = ['正在分析，请稍候...'];

    // 循环查询，直到 response.data.data 存在
    let querySuccess = false;
    while (!querySuccess) {
      try {
        const queryResponse = await axios.get(
          `https://api.coze.cn/v3/chat/message/list?conversation_id=${conversation_id}&chat_id=${chat_id}&`,
          {
            headers: {
              Authorization: 'Bearer pat_r26vcxpAo92sJ5ivwYHAsCzyvz8BsUn35VO9j3XT8dprSvmBVJaCuV3yaCCAluZG',
              'Content-Type': 'application/json'
            }
          }
        );

        console.log('Query Response:', queryResponse.data);

        if (queryResponse.data.data && queryResponse.data.data[4]) {
          messages.value = [queryResponse.data.data[3].content];
          querySuccess = true; // 退出循环
        } else {
          await new Promise(resolve => setTimeout(resolve, 1000)); // 等待 1 秒后重试
        }
      } catch (error) {
        console.error('查询失败:', error);
        await new Promise(resolve => setTimeout(resolve, 1000)); // 等待 1 秒后重试
      }
    }
  } catch (error) {
    console.error('请求失败:', error);
    messages.value = ['请求失败，目前有其他对话在进行，请稍后再试'];
  }
};

// 在组件挂载时确保 fetchDataWithTypingEffect 在 getVegetable 之后执行
onMounted(async () => {
  await getVegetable(); // 等待 getVegetable 完成
  fetchDataWithTypingEffect(); // 再执行 fetchDataWithTypingEffect
});

const processedMessages = computed(() => {
  const sanitizedMessages = messages.value.map(text => {
    // 1. 将 Markdown 转换为 HTML
    const html = marked.parse(text);
    // 2. 安全清理 HTML，允许公式渲染所需的标签
    return DOMPurify.sanitize(html, {
      ALLOWED_TAGS: ['h1', 'h2', 'h3', 'h4', 'p', 'a', 'img', 'strong', 'em', 'ul', 'ol', 'li', 'br', 'span'], // 允许 span 标签
      ALLOWED_ATTR: ['href', 'target', 'src', 'alt', 'class'], // 允许 class 属性
      ALLOWED_CLASSES: {
    'span': ['math-inline', 'math-display'] // 允许 MathJax 的 class
    }
    });
    
  });

  // 确保 DOM 更新后执行 MathJax 渲染
  nextTick(() => {
    if (MathJax.typesetPromise) {
      MathJax.typesetPromise().catch(err => {
        console.error('MathJax 渲染失败:', err);
      });
    }
  });

  return sanitizedMessages;
});


</script>

<template>
  <!-- 添加父容器（如果尚未存在） -->
  <div class="parent-container">
    <el-card class="box-card">
      <div class="card-content">
        <!-- 循环渲染消息 -->
        <div 
          v-for="(message, index) in processedMessages" 
          :key="index" 
          v-html="message"
        ></div>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
/* 基础容器 */
.parent-container {
  background: linear-gradient(135deg, #f8faff 0%, #e7f0ff 100%) !important;
  min-height: 100vh;
  display: flex; /* 使用 flexbox 布局 */
  justify-content: center; /* 水平居中 */
  padding: 30px 20px;
}

.box-card {
  width: 80%; /* 设置宽度为父容器的 80% */
  background: rgba(255, 255, 255, 0.95) !important;
  border: 1px solid #d0e2ff !important;
  box-shadow: 0 8px 24px rgba(66, 133, 244, 0.12) !important;
  border-radius: 16px;
  backdrop-filter: blur(8px);
}

/* 标题层级系统 */
.box-card :deep(h3) {
  font-size: 1.4em;
  color: #2c7be5;
  padding: 12px 20px;
  background: linear-gradient(90deg, #f0f6ff 0%, #e8f3ff 100%);
  border-left: 4px solid #2c7be5;
  margin: 28px -20px 20px;
  box-shadow: inset 0 2px 4px rgba(44,123,229,0.08);
}

.box-card :deep(h4) {
  font-size: 1.25em;
  color: #408de4;
  position: relative;
  padding-bottom: 8px;
  margin: 24px 0 16px;
}

.box-card :deep(h4)::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 48px;
  height: 2px;
  background: linear-gradient(90deg, #4a90e2 0%, #8ab8ff 100%);
}

/* 列表系统 */
.box-card :deep(ul),
.box-card :deep(ol) {
  padding-left: 32px;
  margin: 16px 0;
  border-left: 2px solid #e1ebff;
}

.box-card :deep(li) {
  color: #3c4858;
  margin: 8px 0;
  padding: 6px 12px;
  transition: all 0.2s;
}

.box-card :deep(li:hover) {
  background: #f5f9ff;
  transform: translateX(4px);
}

.box-card :deep(li::marker) {
  color: #8ab8ff;
}

/* 强调文本 */
.box-card :deep(strong) {
  color: #0052cc !important;
  background: linear-gradient(120deg, #e6f0ff 25%, #f0f6ff 75%);
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
}

/* 数学公式 */
.box-card :deep(.math-inline) {
  font-family: "Fira Code", monospace;
  color: #3366ff;
  background: rgba(51,102,255,0.08);
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid rgba(51,102,255,0.15);
}

/* 代码块高亮 */
.box-card :deep(pre) {
  background: #f8faff !important;
  border: 1px solid #d0e2ff !important;
  border-radius: 8px;
  box-shadow: inset 0 2px 6px rgba(44,123,229,0.06);
}

/* 交互增强 */
.box-card :deep(a) {
  color: #3366ff;
  border-bottom: 2px dotted rgba(51,102,255,0.3);
  transition: all 0.2s;
}

.box-card :deep(a:hover) {
  color: #0047b3;
  border-bottom-style: solid;
  background: rgba(51,102,255,0.05);
}

/* 响应式优化 */
@media (max-width: 992px) {
  .box-card {
    width: 95% !important;
    border-radius: 12px;
  }
  
  .box-card :deep(h3) {
    font-size: 1.3em;
    margin: 24px -15px 16px;
  }
  
  .box-card :deep(h4) {
    font-size: 1.15em;
  }
}

/* 动态效果 */
.box-card :deep(*) {
  transition: 
    color 0.3s ease,
    background 0.3s ease,
    transform 0.2s ease;
}
</style>

