<template>
    <div class="overflow-x-hidden">
        <div class="breadcrumbs text-lm size-fit my-6 mx-10">
            <ul>
                <li><a @click="goBack">Home</a></li>
                <li>Create Activity</li>
            </ul>
        </div>
        <div
            class="card p-6 bg-base-300 border-2 border-primary shadow-md rounded-lg m-6"
        >
            <div class="card-body p-4">
                <h2 class="card-title text-2xl mr-2 text-base-content">
                    Create Activity
                </h2>
                <div class="form-control w-full">
                    <div class="label">
                        <span class="text-base-content text-lg">
                            Activity Title
                        </span>
                        <span
                            id="name-field-error"
                            class="text-error text-sm"
                            hidden
                        >
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
                <div
                    v-if="images.length > 0"
                    class="flex flex-col justify-center"
                >
                    <span class="text-base-content text-lg">
                        Preview Image
                    </span>
                    <ImageCarousel
                        :images="images"
                        :removable="true"
                        carouselName="create-activity-carousel"
                        @onRemove="(index) => images.splice(index, 1)"
                    />
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
                        >Up to {{ MAX_IMAGES_SIZE / 1e6 }} MB</span
                    >
                </div>

                <div class="form-control w-full">
                    <div class="label">
                        <span class="text-base-content"> Activity Detail </span>
                        <span
                            id="detail-field-error"
                            class="text-error text-sm"
                            hidden
                        >
                            required
                        </span>
                    </div>
                    <textarea
                        v-model="activityDetail"
                        id="detail-field"
                        class="textarea textarea-primary w-full mb-4 resize-none"
                        placeholder="Activity Detail"
                        :maxlength="1024"
                        :rows="4"
                    >
                    </textarea>
                </div>
                <strong class="text-lg">On-Site</strong>
                <input type="checkbox" class="toggle" @change="toggleOnSite" />
                <div v-if="onSite">
                    <strong class="text-lg">Location</strong>
                    <div class="flex justify-center rounded-lg overflow-hidden">
                        <PickerMapComponent 
                            class="w-[100%] h-[50vh] text-black"
                            @markerPlaced="handleMarkerPlace"
                            :latitude="latitude"
                            :longitude="longitude"
                            />
                    </div>
                </div>

                <div class="form-control w-full">
                    <div class="label">
                        <span class="text-base-content">
                            Activity End Registration Date
                        </span>
                        <span
                            id="end-reg-date-field-error"
                            class="text-error text-sm"
                            hidden
                        >
                            required
                        </span>
                    </div>
                    <VueDatePicker
                        v-model="endRegistrationDate"
                        id="end-reg-date-field"
                        type="text"
                        placeholder="Select End Registration Date"
                        :min-date="new Date()"
                        :dark="isDarkTheme"
                    />
                </div>

                <div class="form-control w-full">
                    <div class="label">
                        <span class="text-base-content">
                            Activity Start Date
                        </span>
                        <span
                            id="date-field-error"
                            class="text-error text-sm"
                            hidden
                        >
                            required
                        </span>
                    </div>
                    <VueDatePicker
                        v-model="date"
                        id="date-field"
                        type="text"
                        placeholder="Select Start Date"
                        :min-date="new Date()"
                        :dark="isDarkTheme"
                    />
                </div>

                <div class="form-control w-full">
                    <div class="label">
                        <span class="text-base-content">
                            Activity End Date
                        </span>
                        <span
                            id="end-date-field-error"
                            class="text-error text-sm"
                            hidden
                        >
                            required
                        </span>
                    </div>
                    <VueDatePicker
                        v-model="endDate"
                        id="end-date-field"
                        type="text"
                        placeholder="Select End Date"
                        :min-date="new Date()"
                        :dark="isDarkTheme"
                    />
                </div>
                <label>Max People </label>
                <input type="checkbox" class="toggle" @change="toggleMaxPeople" />
                <input
                    v-if="showMaxPeople"
                    id="max-field"
                    v-model.number="maxPeople"
                    type="number"
                    placeholder="Enter Max People (Optional)"
                    class="input input-bordered input-primary w-full mb-4"
                    min="1"
                />
                <label>Minimum reputation level </label>
                <input type="checkbox" class="toggle" @change="toggleMinRep" />
                <input
                    v-if="showMinRep"
                    id="min-rep-field"
                    v-model.number="minRep"
                    type="number"
                    placeholder="Enter minimum reputation score (Optional)"
                    class="input input-bordered input-primary w-full mb-4"
                    min="0"
                    max="10"
                />
                <div class="flex flex-col sm:ref(flex-row justify-between">
                    <button
                        v-if="!isAuth"
                        class="btn btn-primary"
                        @click="login"
                    >
                        Please Login before create
                    </button>
                    <button
                        v-else
                        class="btn btn-primary sm:my-0 my-6"
                        @click="postCreateActivity"
                    >
                        Create Activity
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { userId } from '@/functions/Authentications';
import { ref, onMounted } from 'vue';
import { addAlert } from '@/functions/AlertManager';
import { createPostRequest } from '@/functions/HttpRequest';
import { isAuth, login } from '@/functions/Authentications';
import { loadImage } from '@/functions/Utils';
import ImageCarousel from '@/component/ImageCarousel';
import { useRouter } from 'vue-router';
import PickerMapComponent from '@/component/PickerMapComponent.vue';

const MAX_IMAGE_COUNT = 10;
const MAX_IMAGES_SIZE = 100e6; // 100 MB

const router = useRouter();

const activityName = ref('');
const activityDetail = ref('');
const date = ref('');
const endRegistrationDate = ref('');
const endDate = ref('');
const maxPeople = ref(1);
const showMaxPeople = ref(false);
const isDarkTheme = ref(false);
const images = ref([]);
const showMinRep = ref(false);
const minRep = ref(0)

const onSite = ref(false);
const latitude = ref(null);
const longitude = ref(null);

/**
 * Redirection
 */

const goBack = () => {
    /*
     * Navigate back to Activity Index page.
     */
    router.push('/');
};

/**
 * Validator
 */

const validateInput = () => {
    /**
     * Validate input in the forms
     * @return input validity in boolean
     */
    var result = true;
    const nameField = document.getElementById('name-field');
    const nameFieldError = document.getElementById('name-field-error');
    if (activityName.value.length <= 0) {
        nameField.classList.remove('input-primary');
        nameField.classList.add('input-error');
        nameFieldError.removeAttribute('hidden');
        result = false;
    } else {
        nameFieldError.setAttribute('hidden', 'true');
        nameField.classList.remove('input-error');
        if (!nameField.classList.contains('textarea-primary'))
            nameField.classList.add('textarea-primary');
    }
    const detailField = document.getElementById('detail-field');
    const detailFieldError = document.getElementById('detail-field-error');
    if (activityDetail.value.length <= 0) {
        detailField.classList.remove('textarea-primary');
        detailField.classList.add('input-error');

        detailFieldError.removeAttribute('hidden');
        result = false;
    } else {
        detailFieldError.setAttribute('hidden', 'true');
        detailField.classList.remove('input-error');
        if (!detailField.classList.contains('textarea-primary'))
            detailField.classList.add('textarea-primary');
    }
    const dateFieldError = document.getElementById('date-field-error');
    if (date.value.length <= 0) {
        dateFieldError.removeAttribute('hidden');
        result = false;
    } else {
        dateFieldError.setAttribute('hidden', 'true');
    }
    const endRegDateFieldError = document.getElementById(
        'end-reg-date-field-error'
    );
    if (endRegistrationDate.value.length <= 0) {
        endRegDateFieldError.removeAttribute('hidden');
        result = false;
    } else {
        endRegDateFieldError.setAttribute('hidden', 'true');
    }
    const endDateFieldError = document.getElementById('end-date-field-error');
    if (endDate.value.length <= 0) {
        endDateFieldError.removeAttribute('hidden');
        result = false;
    } else {
        endDateFieldError.setAttribute('hidden', 'true');
    }
    if (maxPeople.value <= 0 && showMaxPeople.value) {
        addAlert('warning', 'Max People must be positive and not zeroes.');
        maxPeople.value = 1;
        result = false;
    }
    if (minRep.value < 0 || minRep.value > 10){
        addAlert('warning', 'Max People must be positive and not zeroes.');
        minRep.value = 0;
        result = false;
    }
    if (
        date.value >= endDate.value ||
        endRegistrationDate.value >= endDate.value
    ) {
        addAlert(
            'warning',
            'Start date and end registration date has to come before end date.'
        );
        result = false;
    }

    if (onSite.value && !(latitude.value && longitude.value)) {
        addAlert(
            'warning',
            'Please Place the marker on the map.'
        )
        result = false;
    }

    return result;
};

const toggleMaxPeople = () => {
    /*
     * Switch the flag of setting max people.
     */
    showMaxPeople.value = !showMaxPeople.value;
};

const toggleOnSite = () => {
    /**
     * Toggle the flag of setting onSite
     */
    onSite.value = !onSite.value
}

const toggleMinRep = () => {
    /*
     * Switch the flag of setting minimum reputation.
     */
    showMinRep.value = !showMinRep.value;
};


const handleFileChange = (event) => {
    /*
     * Push value into images.
     * @params {image} image that uploads from input.
     * Return nothing.
     */
    const files = event.target.files;
    if (files.length <= 0) return; // No file to process

    // Check total image count
    if (files.length + images.value.length > MAX_IMAGE_COUNT) {
        addAlert(
            'warning',
            'You can add at most ' + MAX_IMAGE_COUNT + ' pictures'
        );
        return;
    }

    // Calculate total size of current and new images
    let totalSize = images.value.reduce((sum, file) => sum + file.size, 0);

    Array.from(files).forEach((file) => {
        totalSize += file.size;
    });

    // Check if total size exceeds limit
    if (totalSize > MAX_IMAGES_SIZE) {
        addAlert(
            'warning',
            'You can add at most ' + MAX_IMAGES_SIZE / 1e6 + ' MB'
        );
        return; // Return to prevent further execution
    }

    // Process each file
    Array.from(files).forEach((file) => {
        if (file.type.startsWith('image/')) {
            loadImage(file)
                .then((imageSrc) => {
                    // Check for duplicate image URL
                    const isDuplicate = images.value.some(
                        (image) => image === imageSrc
                    );
                    if (!isDuplicate) {
                        images.value.push(imageSrc); // Store the image source in the array
                    } else {
                        addAlert('warning', 'This image is already added.');
                    }
                })
                .catch((error) => {
                    addAlert('error', 'Error loading image: ' + error);
                });
        } else {
            addAlert('warning', file.name + ' is not an image.');
        }
    });
};

const handleMarkerPlace = (coords) => {
    latitude.value = coords.lat;
    longitude.value = coords.lon;
}

/**
 * Submit
 */
const postCreateActivity = async () => {
    /*
     * Attempt to create activity.
     */
    if (!validateInput()) {
        return;
    }
    try {
        // Construct data to create POST request
        const dateObj = new Date(date.value);
        const endRegDateObj = new Date(endRegistrationDate.value);
        const endDateObj = new Date(endDate.value);
        const formattedDate = dateObj.toISOString();
        const formattedEndRegDate = endRegDateObj.toISOString();
        const formattedEndDate = endDateObj.toISOString();

        if (!showMaxPeople.value) {
            maxPeople.value = null;
        }
        let data = {
            name: activityName.value,
            detail: activityDetail.value,
            date: formattedDate,
            end_registration_date: formattedEndRegDate,
            end_date: formattedEndDate,
            max_people: maxPeople.value || null,
            images: images.value,
            owner: userId.value,
            minimum_reputation_score: minRep.value * 10
        };

        if (!onSite.value) {
            data = {
                ...data,
                onsite: false,
            }
        } else {
            data = {
                ...data,
                onsite: true,
                location: {
                    lat: latitude.value,
                    lon: longitude.value
                }
            }
        }
        console.log(data);
        const response = await createPostRequest(`/activities/`, data);
        addAlert('success', response.data.message);
        router.push(`/activities/${response.data.id}`);
    } catch (error) {
        if (error.response && error.response.data) {
            addAlert('error', error.response.data.message); // Show error message from backend
        } else {
            console.error(error);
            addAlert(
                'error',
                'An unexpected error occurred. Please try again later.'
            );
        }
    }
};

onMounted(() => {
    isDarkTheme.value = window.matchMedia(
        '(prefers-color-scheme: dark)'
    ).matches;
    window
        .matchMedia('(prefers-color-scheme: dark)')
        .addEventListener('change', (e) => {
            isDarkTheme.value = e.matches;
        });
});
</script>
