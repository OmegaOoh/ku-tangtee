import { createRouter, createWebHistory } from "vue-router";
import ActivityIndex from "../views/ActivityIndex.vue";
import ActivityDetail from "../views/ActivityDetail.vue";

// Just like  urls.py
const routes = [
    {
        path: "/",
        name: "ActivityIndexPage",
        component: ActivityIndex,
    },
    {
        path: "/activities/:id",
        name: "ActivityDetailPage",
        component: ActivityDetail,
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
