<template>
    <div  v-if="checkInAllowed">
        <h1 @allow-checked-in="fetchCheckInCode" class="card-title text-4xl mr-2 text-base-content align-center">Check-In code: </h1>
        <br>
        <h1 class="card-title text-8xl mr-2 align-center text-accent">{{ this.activity.check_in_code }}</h1>
        <br>
        <button 
            @click="closeCheckIn"
            type="button" 
            class="btn btn-error"
        >
            Close Check-in
        </button>
    </div>
    <div  v-else>
        <button
            @click="allowCheckIn"
            class="btn btn-accent ml-2 mr-2"
        >
            Get Check-In code
        </button>
    </div>
</template>

<script>
import apiClient from "@/api";
import { addAlert } from "@/functions/AlertManager";
import { createPutRequest } from "@/functions/HttpRequest.js";

export default {
    data() {
        return {
            id: this.activityId,
            activity: {},
            checkInCode: "",
            checkInAllowed: false
        };
    },
    methods: {
        async fetchCheckInCode() {
            /*
             * Get data from specific activity including participant detail.
             */
            try {
                const response = await apiClient.get(
                    `/activities/${this.activityId}`
                );
                this.activity = response.data;
                this.checkInCode = this.activity.check_in_code
                this.checkInAllowed = this.activity.check_in_allowed
            } catch (error) {
                console.error("Error fetching activity:", error);
                addAlert(
                    "warning",
                    "Activity already started or No such activity."
                );
            }
        },
        async allowCheckIn() {
            /*
             * Attempt to join activity.
             */
            try {
                const response = await createPutRequest(
                    `/activities/check-in/${this.activityId}/?status=open`,
                    {}
                );
                addAlert("success", response.data.message);
                this.$emit("allow-checked-in")
                this.fetchCheckInCode();
            } catch (error) {
                if (error.response && error.response.data) {
                    addAlert("error", error.response.data.message); // Show error message from backend
                } else {
                    addAlert(
                        "error",
                        "An unexpected error occurred. Please try again later."
                    );
                }
            }
        },
        async closeCheckIn() {
            /**
             * Make check-in unavailable.
             */
            // 
            try {
                const response = await createPutRequest(
                    `/activities/check-in/${this.activityId}/?status=close`,
                    {}
                );
                addAlert("success", response.data.message);
                this.$emit("closed-checked-in")
                this.fetchCheckInCode(); //Fetch Activity
            } catch (error) {
                console.error("Error fetching activity:", error);
                addAlert(
                    "warning",
                    "Activity already started or No such activity."
                );
            }
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
        this.fetchCheckInCode();
    },
};
</script>
