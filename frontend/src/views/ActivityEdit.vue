<template>
    <div class="flex items-center justify-center min-h-screen">
        <div
            class="card bg-neutral card-primary size-1/3 shadow-xl items-center"
        >
            <div class="card-body size-3/4">
                <h2 class="card-title">Edit Activity</h2>
                <label>Activity Name </label>
                <input
                    v-model="activityName"
                    type="text"
                    placeholder="Enter activity name"
                    class="input input-bordered input-primary w-full mb-4"
                    :maxlength="255"
                    required
                />
                <label>Activity Detail </label>
                <textarea
                    v-model="activityDetail"
                    class="textarea textarea-primary w-full mb-4"
                    placeholder="Enter activity detail"
                    :maxlength="1024"
                ></textarea>

                <label>Date and Time </label>
                <VueDatePicker
                    v-model="date"
                    type="text"
                    placeholder="Select Date"
                    :min-date="new Date()"
                    :dark="isDarkTheme"
                />
                <label>Max People </label>
                <input
                    v-model.number="maxPeople"
                    type="number"
                    placeholder="Enter Max People (Optional)"
                    class="input input-bordered input-primary w-full mb-4"
                    :min="0"
                />
                <label>Number of participants </label>
                <input
                    v-model.number="people"
                    type="number"
                    placeholder="Enter People"
                    class="input input-bordered input-primary w-full mb-4"
                    :min="0"
                />
                <button class="btn btn-accent" @click="postUpdateActivity">
                    Update Activity
                </button>
                <button class="btn btn-primary" @click="goBack">
                    Back to List
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import apiClient from "@/api";
export default {
    data() {
        return {
            id: this.activityId,
            activityName: "",
            activityDetail: "",
            date: "",
            maxPeople: 0,
            people: 0,
            showMaxPeople: false,
            isDarkTheme: false,
            activity: {},
        };
    },
    methods: {
        goBack() {
            /*
             * Navigate back to Activity Detail page.
             * This function does not return anything.
             */
            this.$router.push(`/`);
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
                this.activityName = this.activity.name;
                this.activityDetail = this.activity.detail;
                this.date = new Date(this.activity.date);
                this.maxPeople = this.activity.max_people || 0;
                this.showMaxPeople = this.maxPeople > 0;
                this.people = this.activity.people;
            } catch (error) {
                console.error("Error fetching activity:", error);
            }
        },
        async postUpdateActivity() {
            /*
             * Attempt to update activity information.
             * This function does not return anything.
             */
            // Validate numeric input
            if (this.maxPeople < 0) {
                this.maxPeople = 0;
            }
            const csrfResponse = await apiClient.get(
                `/activities/get-csrf-token`
            ); // Ensure this points to the correct endpoint
            const csrfToken = csrfResponse.data.csrfToken;
            try {
                // Construct data to create POST request
                const data = {
                    name: this.activityName,
                    detail: this.activityDetail,
                    date: this.date,
                    max_people: this.maxPeople || null,
                    people: this.people,
                };
                const response = await apiClient.post(
                    `/activities/${this.activityId}/edit`,
                    data,
                    this.activityId,
                    {
                        // HTTP headers
                        headers: { "X-CSRFToken": csrfToken },
                        withCredentials: true,
                    }
                );
                alert(response.data.message);
                this.$router.push(`/activities/${response.data.id}`);
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
        setMaxPeople() {
            this.showMaxPeople = !this.showMaxPeople;
        },
    },
    mounted() {
        this.activityId = this.$route.params.id;
        this.isDarkTheme = window.matchMedia(
            "(prefers-color-scheme: dark)"
        ).matches;
        window
            .matchMedia("(prefers-color-scheme: dark)")
            .addEventListener("change", (e) => {
                this.isDarkTheme = e.matches;
            });
        this.fetchActivity();
    },
};
</script>
