<template>
    <div class="flex items-center justify-center min-h-screen">
        <div
            class="card bg-neutral card-primary size-1/3 shadow-xl items-center"
        >
            <div class="card-body size-3/4">
                <h2 class="card-title">Create Activity</h2>
                <label>Activity Name </label>
                <input
                    v-model="activityName"
                    type="text"
                    placeholder="Activity Name"
                    class="input input-bordered input-primary w-full mb-4"
                    :maxlength="255"
                    required
                />
                <label>Activity Detail </label>
                <textarea
                    v-model="activityDetail"
                    class="textarea textarea-primary w-full mb-4"
                    placeholder="Activity Detail"
                    :maxlength="1024"
                >
                </textarea>

                <label>Date and Time </label>
                <VueDatePicker
                    v-model="date"
                    type="text"
                    placeholder="Select Date"
                    :min-date="new Date()"
                    :dark="isDarkTheme"
                />
                <label>Max People </label>
                <input type="checkbox" class="toggle" @change="setMaxPeople" />
                <input
                    v-if="showMaxPeople"
                    v-model.number="maxPeople"
                    type="number"
                    placeholder="Enter Max People (Optional)"
                    class="input input-bordered input-primary w-full mb-4"
                    :min="0"
                />
                <button class="btn btn-accent" @click="postCreateActivity">
                    Create Activity
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
            activityName: "",
            activityDetail: "",
            date: "",
            maxPeople: 0,
            showMaxPeople: false,
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
        async fetchTimeZoneOffset() {
            try {
                const response = await apiClient.get(
                    "activities/get-timezone/"
                );
                this.timeZoneOffset = response.data.offset; // Set the time zone offset
            } catch (error) {
                console.error("Error fetching time zone offset:", error);
            }
        },
        async postCreateActivity() {
            /*
             * Attempt to create activity.
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
                const dateObj = new Date(this.date);
                const offsetMilliseconds = this.timeZoneOffset * 60 * 60 * 1000;
                const localDate = new Date(
                    dateObj.getTime() + offsetMilliseconds
                );
                const formattedDate = localDate.toISOString();
                const data = {
                    name: this.activityName,
                    detail: this.activityDetail,
                    date: formattedDate,
                    max_people: this.maxPeople || null,
                };
                const response = await apiClient.post(
                    `/activities/create`,
                    data,
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
