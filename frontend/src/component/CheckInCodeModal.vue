<template>
    <h1 class="card-title text-4xl mr-2 text-base-content align-center">Check-In code: </h1>
    <br>
    <h1 class="card-title text-8xl mr-2 align-center text-accent">{{ this.activity.check_in_code }}</h1>
</template>

<script>
import apiClient from "@/api";
import { addAlert } from "@/functions/AlertManager";
export default {
    data() {
        return {
            id: this.activityId,
            activity: {}
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
