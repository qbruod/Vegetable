import { createApp } from 'vue'
import App from './App.vue'
import './index.css'
import '../static/bootstrap5/css/bootstrap.css'
import '../static/bootstrap5/js/bootstrap.bundle.js'
import ElementPlus from 'element-plus'
import router from './router/index.js'
import '/node_modules/element-plus/dist/index.css'


const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.mount('#app')


