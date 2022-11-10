import { createRouter,createWebHashHistory} from "vue-router";

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
      {
        path: '/',
        name: 'Home',
        component: () => import('../views/home.vue'),
      },
      {
        path: '/topic',
        name: 'Topic',
        component: () => import('../views/topic.vue'),
      },
      {
        path: '/login',
        name: 'Login',
        component: () => import('../views/login.vue'),
      },
    ],
  })
  
  export default router