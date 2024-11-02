<template>
    <div class="form-control w-full">
        <div class="label">
            <span class="text-base-content text-lg"> Activity Title </span>
            <span id="code-field-req" class="text-error text-sm" hidden>
                required
            </span>
        </div>
        <div class="label">
            <span class="text-base-content text-lg"> Activity Title </span>
            <span id="code-field-req" class="text-error text-sm" hidden>
                Check in code must have 6 characters
            </span>
        </div>
        <input
            v-model="checkInCode"
            id="check-in-code-fields"
            type="text"
            placeholder="Check-In Code"
            class="input input-bordered input-primary w-full mb-4"
            :maxlength="255"
            required
        />
    </div>
    <div class="flex justify-end">
        <button class="btn btn-accent" @click="postUpdate">
            Update Activity
        </button>
    </div>
</template>

<script>
import apiClient from "@/api";
import { addAlert } from "@/functions/AlertManager";
import { createPostRequest } from "@/functions/HttpRequest.js";

export default {
    data() {
        return {
            id: this.activityId,
            checkInCode: "",
            activity: {}
        };
    },
    methods: {
        async postCheckIn() {
            try {
                const response = await createPostRequest(
                    `/activities/check-in/${this.activityId}/`,
                    {
                        'check_in_code': "yes"
                    }
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
        validateInput() {
            /**
             * Validate input in the forms
             * @return input validity in boolean
             */
            var result = true;
            const nameField = document.getElementById("check-in-code-fields");
            const nameFieldError = document.getElementById("code-field-req");
            if (this.activityName.length <= 0) {
                nameField.classList.remove("input-primary");
                nameField.classList.add("input-error");

                nameFieldError.removeAttribute("hidden");
                result = false;
            }
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
