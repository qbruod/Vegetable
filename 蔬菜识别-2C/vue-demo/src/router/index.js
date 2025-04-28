import {createRouter , createWebHashHistory} from 'vue-router';
import Photo from '../components/Photo.vue'
import Finish from '../components/Finish.vue'
const routes = [
    {
        path:'/photo',
        name:'Photo',
        component: Photo
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
