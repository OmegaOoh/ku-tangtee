<template>
    <div
        class="fixed top-16 left-0 right-0 flex justify-center z-10"
        style="padding: 1%"
    >
        <div
            id="reload"
            class="transform translate-y-0 transition-transform duration-300 ease-in-out"
            hidden
        >
            <button
                class="btn btn-accent size-fit text-xl"
                @click="fetchActivities()"
            >
                ↻ Refresh
            </button>
        </div>
    </div>
    <h1 class="text-4xl font-bold mb-4 flex justify-center my-6">
        Activities List
    </h1>

    <div class="container mx-auto p-4">
        <div class="grid grid-flow-col justify-end pr-5 items-center">
            <div class="flex my-5">
                <input
                    v-model="searchKeyword"
                    @keydown.enter="fetchActivities"
                    class="input input-bordered gap-2 rounded-r-none"
                    placeholder="Search"
                />
                <VueDatePicker
                    v-model="dateRange"
                    id="date-field"
                    type="text"
                    placeholder="Filter by date range"
                    :min-date="null"
                    :max-date="null"
                    :dark="isDarkTheme"
                    range
                    :partial-range="false"
                    class="input input-bordered rounded-none object-full"
                />
                <select
                    v-model="selectedDay"
                    class="input input-bordered rounded-none"
                >
                    <option value="">All Days</option>
                    <option value="1">Sunday</option>
                    <option value="2">Monday</option>
                    <option value="3">Tuesday</option>
                    <option value="4">Wednesday</option>
                    <option value="5">Thursday</option>
                    <option value="6">Friday</option>
                    <option value="7">Saturday</option>
                    <option value="1,7">Weekend</option>
                    <option value="2,3,4,5,6">Weekdays</option>
                </select>
                <button
                    @click="fetchActivities"
                    class="btn btn-secondary rounded-l-none"
                >
                    Search
                </button>
            </div>
        </div>
        <div v-if="activities.length">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div
                    v-for="activity in activities"
                    :key="activity.id"
                    class="card bg-base-300 hover:border-primary border-2 border-base-300 shadow-lg transition-all duration-150"
                >
                    <div class="card-body p-4" style="border-radius: 8px">
                        <h2
                            class="card-title text-2xl font-semibold line-clamp-1"
                        >
                            {{ activity.name }}
                        </h2>
                        <p class="line-clamp-2">{{ activity.detail }}</p>
                        <p>
                            <strong>Date and Time: </strong>
                            {{ formatTimestamp(activity.date) }}
                        </p>
                        <div class="card-actions justify-end">
                            <router-link
                                :to="{ path: `/activities/${activity.id}` }"
                            >
                                <button
                                    class="btn btn-secondary"
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
        <div v-else class="mt-4">
            <div class="card bg-base-300 border-2 border-accent p-5">
                <div class="card-title text-2xl font-semibold">
                    No upcoming activities found.
                </div>
                <div class="card-actions justify-end">
                    <router-link to="/create">
                        <button class="btn btn-accent">Create New!</button>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { format } from "date-fns";
import apiClient from "@/api"; // Get API

export default {
    data() {
        return {
            activities: [],
            isDarkTheme: false,
            timeZoneOffset: 0,
            searchKeyword: "",
            socket: null,
            startDate: null,
            endDate: null,
            dateRange: null,
            selectedDay: null,
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
                let response;
                const params = {};

                // Add parameters only if they have values
                if (this.searchKeyword) {
                    params.keyword = this.searchKeyword;
                }
                if (this.startDate) {
                    params.start_date = format(this.startDate, "yyyy-MM-dd");
                }
                if (this.endDate) {
                    params.end_date = format(this.endDate, "yyyy-MM-dd");
                }
                if (this.selectedDay) {
                    params.day = this.selectedDay;
                }
                console.log(params);
                response = await apiClient.get("/activities/", { params });
                this.activities = response.data;
                window.scrollTo(0, 0);
                // Hide reload button
                const reloadButton = document.getElementById("reload");
                reloadButton.classList.remove("translate-y-0");
                reloadButton.classList.remove("translate-y-[100%]");
                setTimeout(reloadButton.setAttribute("hidden", "true"));
            } catch (error) {
                console.error("Error fetching activities:", error);
                if (error.response) {
                    console.error("Response data:", error.response.data);
                    console.error("Response status:", error.response.status);
                }
            }
        },
        search() {
            /**
             * Handle Search using search bar
             * this function return nothing.
             */
        },
        viewActivity(activityId) {
            /*
             * Navigate to specific activity detail page.
             */
            this.$router.push(`/activities/${activityId}`);
        },
        formatTimestamp(timestamp) {
            /*
             * Format the timestamp into (Oct 22, 2024, 9:00 AM).
             *
             * @params {string} not yet formatted timestamp
             * @returns {string} formatted timestamp
             */
            if (timestamp) {
                return format(new Date(timestamp), "EEE, MMM/dd/yyyy, hh:mm a");
            } else {
                return "No date provided";
            }
        },
        setupSocket() {
            /*
             * Connect to websocket to observe the change of index.
             */
            const socket = new WebSocket(
                `${process.env.VUE_APP_BASE_URL.replace(/^http/, "ws").replace(
                    /^https/,
                    "wss"
                )}ws/index/`
            );
            this.socket = socket;

            this.socket.onmessage = (event) => {
                try {
                    var parsedData = JSON.parse(event.data);
                    if (parsedData["type"] === "new_act") {
                        // Show reload button
                        const reloadButton = document.getElementById("reload");
                        reloadButton.removeAttribute("hidden"); // Show the button
                        reloadButton.classList.remove("translate-y-[-100%]"); // Remove off-screen class
                        reloadButton.classList.add("translate-y-0"); // Slide in
                    }
                } catch (error) {
                    console.log("Parsing Error: ", error);
                }
            };
        },
    },
    beforeUnmount() {
        if (this.socket) {
            this.socket.close();
        }
    },
    watch: {
        dateRange(newRange) {
            this.startDate = newRange ? newRange[0] : null;
            this.endDate = newRange ? newRange[1] : null;
        },
    },
};
</script>

<style scoped>
.line-clamp-2 {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    word-wrap: break-word;
    overflow: hidden;
    text-overflow: ellipsis;
}

.line-clamp-1 {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 1;
    line-clamp: 1;
    word-wrap: break-word;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
