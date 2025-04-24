import {createRouter , createWebHashHistory} from 'vue-router';
import Buy from '../components/Buy.vue'
import Photo from '../components/Photo.vue'
import Finish from '../components/Finish.vue'
const routes = [
    {
        path:'/photo',
        name:'Photo',
        component: Photo
    },
    {
        path:'/buy',
        name:'Buy',
        component: Buy
    },
    {
        path:'/finish',
        name:'Finish',
        component: Finish
    },
];
const router = createRouter({
    history:createWebHashHistory(),
    routes,
});
export default router;
