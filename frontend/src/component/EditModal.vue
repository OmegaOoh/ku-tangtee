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
    <div v-if="images.length > 0" class="flex flex-col justify-center">
        <span class="text-base-content text-lg"> Preview Image </span>
        <div class="">
            <ImageCarousel
                carouselName="edit-carousel"
                :images="images.map((image) => image.url)"
                :removable="true"
                @onRemove="handleRemove"
            />
        </div>
    </div>

    <div>
        <label class="btn btn-primary">
            Add Image
            <input
                type="file"
                multiple
                id="file-add"
                accept="image/*"
                @change="handleFileChange"
                hidden
            />
        </label>
        <span class="text-base-content text-sm ml-2 align-bottom"
            >Up to {{ maxImageCompute() }} MB</span
        >
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
import { loadImage } from "@/functions/Utils.";
import ImageCarousel from "./ImageCarousel.vue";
const MAX_IMAGE_COUNT = 10;
const MAX_IMAGES_SIZE = 100e6; // 100 MB
export default {
    components: {
        ImageCarousel,
    },
    data() {
        return {
            id: this.activityId,
            activityName: "",
            activityDetail: "",
            date: "",
            maxPeople: 0,
            people: [],
            showMaxPeople: false,
            images: [],
            baseUrl: "",
            activity: {},
            new_images: [],
            remove_attachment: [],
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
                this.activityName = this.activity.name;
                this.activityDetail = this.activity.detail;
                this.date = this.formatActivityDate(
                    new Date(this.activity.date)
                );
                this.baseUrl = process.env.VUE_APP_BASE_URL;
                if (this.baseUrl.endsWith("/")) {
                    this.baseUrl = this.baseUrl.slice(0, -1);
                }
                this.images = this.activity.images.map((image) => ({
                    id: image.id,
                    url: `${this.baseUrl}${image.url}`,
                }));
                this.maxPeople =
                    this.activity.max_people || this.activity.people;
                this.showMaxPeople = this.maxPeople > 0;
                this.people = this.activity.participant;
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
                this.new_images = this.images
                    .filter((image) => image.id === -1)
                    .map((image) => image.url);
                const data = {
                    name: this.activityName,
                    detail: this.activityDetail,
                    date: this.date,
                    max_people: this.maxPeople || null,
                    new_images: this.new_images,
                    remove_attachments: this.remove_attachment,
                };
                console.log(this.images);
                const response = await createPutRequest(
                    `/activities/${this.activityId}/`,
                    data
                );
                this.new_images = [];
                this.remove_attachment = [];
                addAlert("success", response.data.message);
                this.$emit("update-success");
                await this.fetchDetail();
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
            /*
             * Swap value of showMaxPeople.
             * Return nothing.
             */
            this.showMaxPeople = !this.showMaxPeople;
        },
        handleFileChange(event) {
            const files = event.target.files;
            if (files.length > 0) {
                // Check total image count
                if (files.length + this.images.length > MAX_IMAGE_COUNT) {
                    addAlert(
                        "warning",
                        "You can add at most " + MAX_IMAGE_COUNT + " pictures"
                    );
                    return;
                }

                // Calculate total size of current and new images
                let totalSize = this.images.reduce(
                    (sum, file) => sum + file.size,
                    0
                );

                Array.from(files).forEach((file) => {
                    totalSize += file.size;
                });

                // Check if total size exceeds limit
                if (totalSize > MAX_IMAGES_SIZE) {
                    addAlert(
                        "warning",
                        "You can add at most " + MAX_IMAGES_SIZE / 1e6 + " MB"
                    );
                    return; // Return to prevent further execution
                }

                // Process each file
                Array.from(files).forEach((file) => {
                    if (file.type.startsWith("image/")) {
                        loadImage(file)
                            .then((imageSrc) => {
                                // Check for duplicate image URL
                                const isDuplicate = this.images.some(
                                    (image) => image.url === imageSrc
                                );
                                if (!isDuplicate) {
                                    this.images.push({ id: -1, url: imageSrc }); // Store the image source in the array
                                } else {
                                    addAlert(
                                        "warning",
                                        "This image is already added."
                                    );
                                }
                            })
                            .catch((error) => {
                                console.error("Error loading image:", error);
                            });
                    } else {
                        addAlert("warning", file.name + " is not an image.");
                    }
                });
            }
        },
        handleRemove(index) {
            /*
             * Remove image and push removed image id into array.
             * @params {int} image that wants to be removed.
             * Return nothing.
             */
            if (this.images[index].id != -1) {
                this.remove_attachment.push(this.images[index].id);
            }
            // Remove the image from the images array
            this.images.splice(index, 1);
        },
        maxImageCompute() {
            /*
             * Compute max image size.
             *
             * @returns {int} max image size in MB
             */
            return MAX_IMAGES_SIZE / 1e6;
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
