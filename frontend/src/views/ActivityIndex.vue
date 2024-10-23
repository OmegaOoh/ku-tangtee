<template>
    <div class="container mx-auto p-4">
        <h1 class="text-4xl font-bold mb-4">Activities List</h1>
        <div id="reload" style="padding: 1%" hidden>
            <button class="btn btn-accent" @click="fetchActivities()">
                New Activity Available!, Reload Now
            </button>
        </div>
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
                        <p class="line-clamp-2">{{ activity.detail }}</p>
                        <p>
                            Start date:
                            {{ formatTimestamp(activity.date) }}
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
import { format } from "date-fns";

export default {
    data() {
        return {
            activities: [],
            isDarkTheme: false,
            timeZoneOffset: 0,
        };
    },
    mounted() {
        this.fetchActivities();
        this.setupSocket();
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
                document.getElementById("reload").setAttribute("hidden", true);
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
        formatTimestamp(timestamp) {
            if (timestamp) {
                return format(new Date(timestamp), "PPp");
            } else {
                return "No date provided";
            }
        },
        setupSocket() {
            /*
             * Connect to websocket to observe the change of index.
             * Return Nothing
             */
            const socket = new WebSocket(
                `${process.env.VUE_APP_BASE_URL.replace(/^http/, "ws").replace(
                    /^https/,
                    "wss"
                )}ws/index/`
            );

            socket.onmessage = (event) => {
                try {
                    var parsedData = JSON.parse(event.data);
                    if (parsedData["type"] === "new_act") {
                        document
                            .getElementById("reload")
                            .removeAttribute("hidden");
                    }
                } catch (error) {
                    console.log("Parsing Error: ", error);
                }
            };
        },
    },
};
</script>
