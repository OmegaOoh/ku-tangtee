import { createRouter, createWebHistory } from "vue-router";
import ActivityIndex from "../views/ActivityIndex.vue";
import ActivityDetail from "../views/ActivityDetail.vue";
import ActivityCreate from "../views/ActivityCreate.vue";
import ActivityEdit from "../component/EditModal.vue";

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
    {
        path: "/activities/:id/edit",
        name: "ActivityEditPage",
        component: ActivityEdit,
    },
    {
        path: "/create",
        name: "ActivityCreationPage",
        component: ActivityCreate,
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
