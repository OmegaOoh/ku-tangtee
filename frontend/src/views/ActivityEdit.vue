<template>
    <div class="flex items-center justify-center">
        <div
            class="card bg-neutral card-primary w-full sm:w-3/4 md:w-1/2 lg:w-1/3 shadow-xl items-center"
        >
            <div class="card-body size-3/4 overflow-auto p-6">
                <h2 class="card-title text-2xl mr-2 white-text">
                    Edit Activity
                </h2>
                <label class="white-text">Activity Name </label>
                <input
                    v-model="activityName"
                    type="text"
                    placeholder="Enter activity name"
                    class="input input-bordered input-primary w-full mb-4"
                    :maxlength="255"
                    required
                />
                <label class="white-text">Activity Detail </label>
                <textarea
                    v-model="activityDetail"
                    class="textarea textarea-primary w-full mb-4"
                    placeholder="Enter activity detail"
                    :maxlength="1024"
                ></textarea>

                <label class="white-text">Date and Time </label>
                <VueDatePicker
                    v-model="date"
                    type="text"
                    placeholder="Select Date"
                    :min-date="new Date()"
                    :dark="isDarkTheme"
                />
                <label class="white-text">Max People </label>
                <input
                    v-model.number="maxPeople"
                    type="number"
                    placeholder="Enter Max People (Optional)"
                    class="input input-bordered input-primary w-full mb-4"
                    :min="0"
                />
                <div class="flex items-center space-x-4">
                    <label class="white-text">Number of participant : </label>
                    <p class="white-text">{{ people.length }}</p>
                </div>
                <label class="white-text">Participant list</label>
                <div class="grid grid-cols-1 md:grid-cols-1 gap-4 mb-2 ml-3">
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
import "@/styles/WhiteText.css";
export default {
    data() {
        return {
            id: this.activityId,
            activityName: "",
            activityDetail: "",
            date: "",
            maxPeople: 0,
            people: [],
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
             * Get data from specific activity including participant detail.
             * This function does not return anything.
             */
            try {
                const response = await apiClient.get(
                    `/activities/${this.activityId}`
                );
                this.activity = response.data;
                const participant = await apiClient.get(
                    `/activities/get-participant/${this.activity.id}/`
                );
                this.activityName = this.activity.name;
                this.activityDetail = this.activity.detail;
                this.date = new Date(this.activity.date);
                this.maxPeople = this.activity.max_people || 0;
                this.showMaxPeople = this.maxPeople > 0;
                this.people = participant.data;
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
            );
            const csrfToken = csrfResponse.data.csrfToken;
            try {
                // Construct data to create POST request
                const data = {
                    name: this.activityName,
                    detail: this.activityDetail,
                    date: this.date,
                    max_people: this.maxPeople || null,
                };
                const response = await apiClient.put(
                    `/activities/${this.activityId}/`,
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
