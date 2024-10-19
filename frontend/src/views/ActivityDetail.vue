<template>
    <div class="p-6 bg-base-100 shadow-md rounded-lg">
        <div class="bg-primary card-body p-4" style="border-radius: 8px">
            <h1 class="text-4xl font-bold mb-4 ml-2">
                {{ activity.name }}
            </h1>
            <p class="mb-2 ml-3">
                <strong class="text-lg">Details:</strong> {{ activity.detail }}
            </p>
            <p class="mb-2 ml-3">
                <strong class="text-lg">Date:</strong>
                {{ formatActivityDate(activity.date) }}
            </p>
            <p class="mb-2 ml-3">
                <strong class="text-lg">Max People:</strong>
                {{ activity.max_people }}
            </p>
            <p class="mb-4 ml-3">
                <strong class="text-lg">Joined People:</strong>
                {{ activity.people }}
            </p>

            <div class="flex justify-between items-center">
                <div class="flex space-x-4">
                    <button @click="goToEdit" class="btn btn-warning ml-2 mr-2">
                        Edit
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
import "@/styles/ActivityDetail.css";
export default {
    data() {
        return {
            activity: {},
            canJoin: true,
            csrfToken: "",
            activityId: null,
            isDarkTheme: false,
            timeZoneOffset: 0,
        };
    },
    methods: {
        goBack() {
            /*
             * Navigate back to Activity Index page.
             * This function does not return anything.
             */
            this.$router.push("/");
        },
        goToEdit() {
            /*
             * Navigagte to Activity Edit page.
             * This function does not return anything.
             */
            this.$router.push(`/activities/${this.activityId}/edit`);
        },
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
             * Get data from specific activity.
             * This function does not return anything.
             */
            try {
                const response = await apiClient.get(
                    `/activities/${this.activityId}`
                );
                this.activity = response.data;
                this.canJoin = this.activity.can_join; // Adjust this based on your backend logic
            } catch (error) {
                console.error("Error fetching activity:", error);
            }
        },
        async joinActivity() {
            /*
             * Attempt to join activity.
             * This function does not return anything.
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
        this.fetchTimeZoneOffset();
    },
};
</script>
