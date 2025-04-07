import { createApp } from 'vue'
import App from './App.vue'
import './index.css'
import '../static/bootstrap5/css/bootstrap.css'
import '../static/bootstrap5/js/bootstrap.bundle.js'
import ElementPlus from 'element-plus'
import '/node_modules/element-plus/dist/index.css'
import router from './router/router'

createApp(App)
.use(ElementPlus)
.use(router)
.mount('#app')

