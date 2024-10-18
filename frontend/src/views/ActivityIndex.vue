<template>
    <div class="container mx-auto p-4">
        <h1 class="text-4xl font-bold mb-4">Activities List</h1>
        <button v-if="newActivities > 0" class ='btn bg-neutral' @click="Location.reload()">
            Reload Page ({{ newActivities }} added)
        </button>
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
                            {{ formatActivityDate(activity.date) }}
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
            timeZoneOffset: 0,
            newActivities: 0,
        };
    },
    mounted() {
        this.fetchTimeZoneOffset();
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
        async fetchTimeZoneOffset() {
            /*
             * Attempt to get timezone offset.
             * This function does not return anything.
             */
            try {
                const response = await apiClient.get(
                    "activities/get-timezone/"
                );
                this.timeZoneOffset = response.data.offset; // Set the time zone offset
            } catch (error) {
                console.error("Error fetching time zone offset:", error);
            }
        },
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
        formatActivityDate(date) {
            /*
             * Adjust the activity date with the timezone offset.
             * Return localized time.
             */
            const dateObj = new Date(date);
            const offsetMilliseconds = this.timeZoneOffset * 60 * 60 * 1000;
            const localDate = new Date(dateObj.getTime() + offsetMilliseconds);
            return localDate.toLocaleString(); // Return the localized date string
        },
        setupSocket(){
            /*
             * Connect to websocket to observe the change of index.
             * Return Nothing
             */
            const socket = new WebSocket(`${process.env.VUE_APP_BASE_URL.replace(/^http/, 'ws')
                                                                        .replace(/^https/, 'wss')}ws/index/`);
            socket.onopen = function(event){
                console.log('index websocket successfully connect.', event);
            }
            socket.onmessage = function(event){
                    try {
                        var parsedData = JSON.parse(event.data);
                        if (parsedData.type == 'newAct')
                            {
                                this.newActivities++;
                            }
                        
                    } catch (error) {
                        console.log('Parsing Error: ', error)
                    }

                socket.onerror = function(e){
                    console.log('Websocket Error', e);
                }
            }
        }
    },
};
</script>
