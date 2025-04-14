import { createRouter, createWebHashHistory } from 'vue-router';
import VegMat from '../components/VegetableManagement.vue'
import VegStk from '../components/VegetableStock.vue'
import VegAge from '../components/VegetableAgent.vue'

const routes=[
    {
        path:'/',
        name:'path',
        component:VegMat
    },
    {
        path:'/VegetableStock',
        name:'vegetableStock',
        component:VegStk
    },
    {
        path:'/VegetableAgent',
        name:'vegetableAgent',
        component:VegAge
    }
];

const router=createRouter({
    history: createWebHashHistory(), // 使用hash路由模式
    routes
})

export default router;
