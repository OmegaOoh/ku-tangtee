import { createRouter, createWebHistory } from 'vue-router';
import ActivityIndex from '@/views/ActivityIndex.vue';
import ActivityDetail from '@/views/ActivityDetail.vue';
import ActivityCreate from '@/views/ActivityCreate.vue';
import ActivityChat from '@/views/ActivityChat.vue';
import ProfileCreate from '@/views/ProfileCreate.vue';
import ProfilePage from '@/views/ProfilePage.vue';
import NotFound from '@/views/PageNotFound.vue'

// Just like  urls.py
const routes = [
    {
        path: '/',
        name: 'ActivityIndexPage',
        component: ActivityIndex,
    },
    {
        path: '/activities/:id',
        name: 'ActivityDetailPage',
        component: ActivityDetail,
    },
    {
        path: '/create',
        name: 'ActivityCreationPage',
        component: ActivityCreate,
    },
    {
        path: '/chat/:id',
        name: 'ActivityChatPage',
        component: ActivityChat,
    },
    {
        path: '/create-profile',
        name: 'ProfileCretePage',
        component: ProfileCreate,
    },
    {
        path: '/profile/:username',
        name: 'ProfilePage',
        component: ProfilePage,
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotfoundPage',
        component: NotFound,
    },
];

const router = createRouter({
    history: createWebHistory(''),
    routes,
});

export default router;
