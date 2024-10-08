<template>
    <div class="activity-detail">
        <h1 class="activity-title">{{ activity.name }}</h1>
        <p class="activity-detail-text">
            <strong>Details:</strong> {{ activity.detail }}
        </p>
        <p class="activity-date">
            <strong>Date:</strong>
            {{ new Date(activity.date).toLocaleString() }}
        </p>
        <p class="activity-max-people">
            <strong>Max People:</strong> {{ activity.max_people }}
        </p>
        <p class="activity-joined-people">
            <strong>Joined People:</strong> {{ activity.people }}
        </p>

        <button v-if="canJoin" @click="joinActivity" class="join-button">
            Join Activity
        </button>
        <p v-else class="cannot-join">This activity cannot be joined.</p>
        <button @click="goToEdit" class="edit-button">Edit</button>
        <button @click="goBack" class="back-button">Back to Activities</button>
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
                    `/activities/${this.activityId}/join`,
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
    },
    mounted() {
        this.activityId = this.$route.params.id;
        this.fetchActivity();
    },
};
</script>
