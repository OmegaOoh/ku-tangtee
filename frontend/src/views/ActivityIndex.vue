<template>
    <div>
        <h1 class="title">Activities List</h1>
        <ul v-if="activities.length">
            <li
                v-for="activity in activities"
                :key="activity.id"
                class="activity-detail"
            >
                <h2 class="activity-title">
                    {{ activity.name }}
                </h2>
                <p class="activity-detail-text">{{ activity.detail }}</p>
                <p class="activity-date">
                    Start date: {{ new Date(activity.date).toLocaleString() }}
                </p>
                <router-link :to="{ path: `/activities/${activity.id}` }">
                    <button
                        @click="viewActivity(activity.id)"
                        class="view-button"
                    >
                        View
                    </button>
                </router-link>
            </li>
        </ul>
        <p v-else>No upcoming activities found.</p>
    </div>
</template>

<script>
import apiClient from "@/api"; // Get API
import "@/styles/ActivityIndex.css";

export default {
    data() {
        return {
            activities: [],
        };
    },
    mounted() {
        this.fetchActivities();
    },
    methods: {
        async fetchActivities() {
            /*
             * Get data for all activities from API.
             */
            try {
                const response = await apiClient.get("/activities/"); // Trying to get data from API
                this.activities = response.data;
            } catch (error) {
                console.error("Error fetching activities:", error);
                if (error.response) {
                    console.error("Response data:", error.response.data);
                    console.error("Response status:", error.response.status);
                }
            }
        },
        viewActivity(activityId) {
            /*
             * Navigate to specific activity detail page.
             */
            this.$router.push(`/activities/${activityId}`);
        },
    },
};
</script>
