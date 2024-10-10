<template>
    <div class="container mx-auto p-4">
        <h1 class="text-4xl font-bold mb-4">Activities List</h1>
        <div v-if="activities.length">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div
                    v-for="activity in activities"
                    :key="activity.id"
                    class="card bg-base-100 shadow-lg hover:shadow-xl transition-shadow duration-200"
                >
                    <div
                        class="bg-primary card-body p-4"
                        style="border-radius: 8px"
                    >
                        <h2 class="card-title text-2xl font-semibold">
                            {{ activity.name }}
                        </h2>
                        <p>{{ activity.detail }}</p>
                        <p>
                            Start date:
                            {{ new Date(activity.date).toLocaleString() }}
                        </p>
                        <div class="card-actions justify-end">
                            <router-link
                                :to="{ path: `/activities/${activity.id}` }"
                            >
                                <button
                                    class="btn btn-info"
                                    @click="viewActivity(activity.id)"
                                >
                                    View
                                </button>
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <p v-else class="text-center text-gray-500 mt-4">
            No upcoming activities found.
        </p>
    </div>
</template>

<script>
import apiClient from "@/api"; // Get API
import "@/styles/ActivityIndex.css";

export default {
    data() {
        return {
            activities: [],
            isDarkTheme: false,
        };
    },
    mounted() {
        this.fetchActivities();
        this.isDarkTheme = window.matchMedia(
            "(prefers-color-scheme: dark)"
        ).matches;
        window
            .matchMedia("(prefers-color-scheme: dark)")
            .addEventListener("change", (e) => {
                this.isDarkTheme = e.matches;
            });
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
