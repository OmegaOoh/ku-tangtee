<template>
    <div class="p-6 bg-base-100 shadow-md rounded-lg">
        <div class="bg-primary card-body p-4" style="border-radius: 8px">
            <h1 class="text-4xl font-bold mb-4 ml-2">
                {{ activity.name }}
            </h1>
            <p class="mb-2 ml-3 overflow-hidden">
                <strong class="text-lg">Details: </strong> {{ activity.detail }}
            </p>
            <p class="mb-2 ml-3">
                <strong class="text-lg">Date: </strong>
                <time class="text-lg">{{
                    formatTimestamp(activity.date)
                }}</time>
            </p>
            <p class="mb-2 ml-3">
                <strong class="text-lg">Max People: </strong>
                {{ activity.max_people }}
            </p>
            <p class="mb-2 ml-3">
                <strong class="text-lg">Joined People: </strong>
            </p>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-2 ml-3">
                <div
                    v-for="participant in people"
                    :key="participant.id"
                    class="card bg-base-100 shadow-lg p-4 rounded-lg"
                >
                    <div class="flex items-center space-x-4">
                        <img
                            :src="participant.profile_picture_url"
                            alt="Profile Picture"
                            class="w-12 h-12 rounded-full"
                        />
                        <p class="font-medium">
                            {{ participant.first_name }}
                            {{ participant.last_name }}
                        </p>
                    </div>
                </div>
            </div>

            <div class="flex justify-between items-center">
                <div class="flex space-x-4">
                    <button @click="goToEdit" class="btn btn-warning ml-2 mr-2">
                        Edit
                    </button>
                    <button
                        @click="goToChat"
                        class="btn btn-secondary ml-2 mr-2"
                    >
                        Chat
                    </button>
                    <button @click="goBack" class="btn btn-info ml-2 mr-2">
                        Back to Activities
                    </button>
                </div>
                <button
                    v-if="canJoin"
                    @click="joinActivity"
                    class="btn btn-success ml-2 mr-2"
                >
                    Join Activity
                </button>
                <p v-else class="text-red-500 mt-4 ml-2 mr-2">
                    This activity cannot be joined.
                </p>
            </div>
        </div>
    </div>
</template>

<script>
import apiClient from "@/api";
import { format } from "date-fns";
export default {
    data() {
        return {
            activity: {},
            canJoin: true,
            csrfToken: "",
            activityId: null,
            isDarkTheme: false,
            timeZoneOffset: 0,
            people: [],
        };
    },
    methods: {
        goBack() {
            /*
             * Navigate back to Activity Index page.
             */
            this.$router.push("/");
        },
        goToEdit() {
            /*
             * Navigagte to Activity Edit page.
             */
            this.$router.push(`/activities/${this.activityId}/edit`);
        },
        goToChat() {
            /*
             * Navigagte to Activity Chart page.
             */
            this.$router.push(`/chat/${this.activityId}`);
        },
        async getCsrfToken() {
            /*
             * Get CSRF Token.
             * @returns {string} CSRF Token.
             */
            const response = await apiClient.get(`/activities/get-csrf-token`); // Ensure this points to the correct endpoint
            return response.data.csrfToken; // Return the CSRF token
        },
        async fetchActivity() {
            /*
             * Get data from specific activity including participant detail.
             */
            try {
                const response = await apiClient.get(
                    `/activities/${this.activityId}`
                );
                this.activity = response.data;
                const participant = await apiClient.get(
                    `/activities/get-participant/${this.activity.id}/`
                );
                this.people = participant.data;
                this.canJoin = this.activity.can_join; // Adjust this based on your backend logic
            } catch (error) {
                console.error("Error fetching activity:", error);
            }
        },
        async joinActivity() {
            /*
             * Attempt to join activity.
             */
            try {
                this.csrfToken = await this.getCsrfToken();
                console.log(this.csrfToken);
                const response = await apiClient.post(
                    `/activities/${this.activityId}/`,
                    {},
                    {
                        headers: { "X-CSRFToken": this.csrfToken },
                        withCredentials: true,
                    }
                );
                alert(response.data.message);
                location.reload(); // Refresh the page
            } catch (error) {
                console.error(
                    "Error details:",
                    error.response ? error.response.data : error
                );
                if (error.response && error.response.data) {
                    alert(error.response.data.error); // Show error message from backend
                } else {
                    alert(
                        "An unexpected error occurred. Please try again later."
                    );
                }
            }
        },
        formatTimestamp(timestamp) {
            /*
             * Format the timestamp into (Oct 22, 2024, 9:00 AM).
             *
             * @params {string} not yet formatted timestamp
             * @returns {string} formatted timestamp
             */
            if (timestamp) {
                return format(new Date(timestamp), "PPp");
            } else {
                return "No date provided";
            }
        },
    },
    mounted() {
        this.activityId = this.$route.params.id;
        this.fetchActivity();
        this.isDarkTheme = window.matchMedia(
            "(prefers-color-scheme: dark)"
        ).matches;
        window
            .matchMedia("(prefers-color-scheme: dark)")
            .addEventListener("change", (e) => {
                this.isDarkTheme = e.matches;
            });
    },
};
</script>
