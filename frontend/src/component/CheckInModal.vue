<template>
    <div class="form-control w-full">
        <div class="label"> 
            <span class="text-base-content text-4xl">Check-In Code: </span>
        </div>
        <div class="label"> 
            <span id="code-field-must-6" class="text-error text-sm" hidden>
                Check-in code must have 6 characters
            </span>
            <span id="invalid-code" class="text-error text-sm" hidden>
                Invalid Check-In code
            </span>
        </div>
        <input
            v-model="checkInCode"
            id="check-in-code-fields"
            type="text"
            class="input input-bordered input-primary w-full mb-4 text-8xl h-fit text-accent"
            :maxlength="6"
            required
        />
    </div>
    <br>
    <div class="flex justify-end">
        <button class="btn btn-accent" @click="postCheckIn">
            Check-In
        </button>
    </div>
</template>

<script>
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
            if (this.validateCheckInCode()){
                try {
                    const response = await createPostRequest(
                        `/activities/check-in/${this.activityId}/`,
                        {
                            'check_in_code': this.checkInCode
                        }
                    );
                    addAlert("success", response.data.message);
                    this.$emit("check-in-success");
                } catch (error) {
                    if (error.response && error.response.data) {
                        if (error.response.data.message == "Check-in code invalid"){
                            const checkInCodeField = document.getElementById("check-in-code-fields");
                            const invalidCodeError = document.getElementById("invalid-code");
                            checkInCodeField.classList.remove("input-primary");
                            checkInCodeField.classList.add("input-error");
                            invalidCodeError.removeAttribute("hidden")
                        } else {
                            addAlert("error", error.response.data.message); // Show error message from backend
                        }

                    } else {
                        addAlert(
                            "error",
                            "An unexpected error occurred. Please try again later."
                        );
                    }
                }
            }
        },
        validateCheckInCode() {
            /**
             * Validate input in the forms
             * @return input validity in boolean
             */

            const checkInCodeField = document.getElementById("check-in-code-fields");
            var result = true;
            var checkInCodeError = document.getElementById("code-field-must-6");
            if (this.checkInCode.length != 6) {
                checkInCodeField.classList.remove("input-primary");
                checkInCodeField.classList.add("input-error");

                checkInCodeError.removeAttribute("hidden");
                result = false;
            }
            return result
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
    },
};
</script>
