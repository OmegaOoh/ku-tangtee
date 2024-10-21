<template>
    <div class="flex items-center justify-center min-h-screen">
        <div class="card bg-neutral card-primary w-1/3 shadow-xl items-center">
            <div class="card-body size-3/4">
                <h2 class="card-title text-2xl mr-2 white-text">
                    Create Activity
                </h2>
                <label class="white-text">Activity Name </label>
                <input
                    v-model="activityName"
                    type="text"
                    placeholder="Activity Name"
                    class="input input-bordered input-primary w-full mb-4"
                    :maxlength="255"
                    required
                />
                <label class="white-text">Activity Detail </label>
                <textarea
                    v-model="activityDetail"
                    class="textarea textarea-primary w-full mb-4"
                    placeholder="Activity Detail"
                    :maxlength="1024"
                >
                </textarea>

                <label class="white-text">Date and Time </label>
                <VueDatePicker
                    v-model="date"
                    type="text"
                    placeholder="Select Date"
                    :min-date="new Date()"
                    :dark="isDarkTheme"
                />
                <label class="white-text">Max People </label>
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
import { createPostRequest } from "@/functions/HttpRequest.js";
import "@/styles/WhiteText.css";
export default {
    data() {
        return {
            activityName: "",
            activityDetail: "",
            date: "",
            maxPeople: 0,
            showMaxPeople: false,
            isDarkTheme: false,
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
        async postCreateActivity() {
            /*
             * Attempt to create activity.
             * This function does not return anything.
             */
            // Validate numeric input
            if (this.maxPeople < 0) {
                this.maxPeople = 0;
            }
            try {
                // Construct data to create POST request
                const dateObj = new Date(this.date);
                const formattedDate = dateObj.toISOString();
                const data = {
                    name: this.activityName,
                    detail: this.activityDetail,
                    date: formattedDate,
                    max_people: this.maxPeople || null,
                };
                const response = await createPostRequest(
                    `/activities/`,
                    data
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
    },
};
</script>
