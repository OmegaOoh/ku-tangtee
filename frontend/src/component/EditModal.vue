<template>
    <h2 class="card-title text-2xl mr-2 text-base-content">Edit Activity</h2>
    <div class="form-control w-full">
        <div class="label">
            <span class="text-base-content text-lg"> Activity Title </span>
            <span id="name-field-error" class="text-error text-sm" hidden>
                required
            </span>
        </div>
        <input
            v-model="activityName"
            id="name-field"
            type="text"
            placeholder="Activity Title"
            class="input input-bordered input-primary w-full mb-4"
            :maxlength="255"
            required
        />
    </div>
    <div class="form-control w-full">
        <div class="label">
            <span class="text-base-content"> Activity Detail </span>
            <span id="detail-field-error" class="text-error text-sm" hidden>
                required
            </span>
        </div>
        <textarea
            v-model="activityDetail"
            id="detail-field"
            class="textarea textarea-primary w-full mb-4"
            placeholder="Activity Detail"
            :maxlength="1024"
        >
        </textarea>
    </div>
    <div class="form-control w-full my-1">
        <div class="label">
            <span class="text-base-content"> Activity Date </span>
            <span id="date-field-error" class="text-error text-sm" hidden>
                required
            </span>
        </div>
        <VueDatePicker
            v-model="date"
            id="date-field"
            type="text"
            placeholder="Select Date"
            :min-date="new Date()"
            :dark="isDarkTheme"
        />
    </div>
    <div class="mt-5">
        <div>
            <label class="text-base-content my-5">Max People</label>
        </div>
        <div class="join">
            <input
                type="checkbox"
                class="toggle"
                @change="setMaxPeople"
                :checked="showMaxPeople"
            />
            <input
                v-if="showMaxPeople"
                id="max-field"
                v-model.number="maxPeople"
                type="number"
                placeholder="Enter Max People (Optional)"
                class="input input-bordered input-primary w-full mb-4"
                :min="activity.people"
            />
        </div>
    </div>

    <div class="flex justify-end">
        <button class="btn btn-accent" @click="postUpdate">
            Update Activity
        </button>
    </div>
</template>

<script>
import apiClient from "@/api";
import { createPutRequest } from "@/functions/HttpRequest.js";
import { addAlert } from "@/functions/AlertManager";
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

            activity: {},
        };
    },
    methods: {
        async fetchDetail() {
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
                this.date = this.formatActivityDate(
                    new Date(this.activity.date)
                );
                this.maxPeople =
                    this.activity.max_people || this.activity.people;
                this.showMaxPeople = this.maxPeople > 0;
                this.people = participant.data;
            } catch (error) {
                console.error("Error fetching activity:", error);
            }
        },
        validateInput() {
            /**
             * Validate input in the forms
             * @return input validity in boolean
             */
            var result = true;
            const nameField = document.getElementById("name-field");
            const nameFieldError = document.getElementById("name-field-error");
            if (this.activityName.length <= 0) {
                nameField.classList.remove("input-primary");
                nameField.classList.add("input-error");

                nameFieldError.removeAttribute("hidden");
                result = false;
            } else {
                nameFieldError.setAttribute("hidden", "true");
                nameField.classList.remove("input-error");
                if (!nameField.classList.contains("textarea-primary"))
                    nameField.classList.add("textarea-primary");
            }
            const detailField = document.getElementById("detail-field");
            const detailFieldError =
                document.getElementById("detail-field-error");
            if (this.activityDetail.length <= 0) {
                detailField.classList.remove("textarea-primary");
                detailField.classList.add("input-error");

                detailFieldError.removeAttribute("hidden");
                result = false;
            } else {
                detailFieldError.setAttribute("hidden", "true");
                detailField.classList.remove("input-error");
                if (!detailField.classList.contains("textarea-primary"))
                    detailField.classList.add("textarea-primary");
            }
            const dateFieldError = document.getElementById("date-field-error");
            if (this.date.length <= 0) {
                dateFieldError.removeAttribute("hidden");
                result = false;
            } else {
                dateFieldError.setAttribute("hidden", "true");
            }
            if (this.maxPeople < this.activity.people) {
                addAlert(
                    "warning",
                    "Max People must be higher or equal to current participants."
                );
                this.maxPeople = this.activity.people;
                result = false;
            }
            return result;
        },
        async postUpdate() {
            /*
             * Attempt to update activity information.
             * This function does not return anything.
             */

            if (!this.validateInput()) {
                return;
            }
            try {
                // Construct data to create POST request
                if (!this.showMaxPeople) {
                    this.maxPeople = null;
                }
                const data = {
                    name: this.activityName,
                    detail: this.activityDetail,
                    date: this.date,
                    max_people: this.maxPeople || null,
                };
                const response = await createPutRequest(
                    `/activities/${this.activityId}/`,
                    data
                );
                addAlert("success", response.data.message);
                this.$emit("update-success");
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
        formatActivityDate(date) {
            /*
             * Adjust the activity date with the timezone offset.
             * Return localized time.
             */
            const dateObj = new Date(date);
            return dateObj;
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
        this.fetchDetail();
    },
};
</script>
