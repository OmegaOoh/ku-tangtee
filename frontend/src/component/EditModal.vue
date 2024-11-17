<template>
    <div
        v-if="isOpen"
        id="edit-modal"
        class="fixed inset-0 flex items-center justify-center backdrop-blur-md bg-black bg-opacity-40 z-10 transition-all ease-in-out duration-200"
        @click="closeModal"
    >
        <div
            class="rounded-lg p-4 relative card bg-base-300 border-2 border-primary w-[75%] h-[80vh] overflow-y-auto"
            @click.stop
        >
            <h2 class="card-title text-2xl mr-2 text-base-content">
                Edit Activity
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

            <p>On-Site</p>
            <input 
                type="checkbox" 
                class="toggle mb-2" 
                @change="toggleOnSite" 
                :checked="activity.on_site"
            />
            <div v-if="activity.on_site">
                <div class="flex justify-center rounded-lg overflow-hidden">
                    <PickerMapComponent 
                        class="w-[100%] h-[50vh] text-black"
                        @markerPlaced="handleMarkerPlace"
                        :latitude="activity.location.lat"
                        :longitude="activity.location.lon"
                        @markerPlace = "handleMarkerPlace"
                        />
                </div>
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
                    rows="3"
                >
                </textarea>
            </div>
            <div class="form-control w-full my-1">
                <div class="label">
                    <span class="text-base-content"> Activity Start Date </span>
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
                    placeholder="Select Date"
                    :min-date="new Date()"
                    :dark="isDarkTheme"
                />
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
                    <span class="text-base-content"> Activity End Date </span>
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
            <div class="mt-5">
                <div>
                    <label class="text-base-content my-5">Max People</label>
                </div>
                <div class="join">
                    <input
                        type="checkbox"
                        class="toggle"
                        @change="toggleMaxPeople"
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
                <div>
                    <label>Minimum reputation level </label>
                </div>
                <div class="join">
                    <input type="checkbox" class="toggle" @change="setMinRep" />
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
                </div>
            </div>

            <div class="flex justify-end">
                <button class="btn btn-accent" @click="postUpdate">
                    Update Activity
                </button>
            </div>

            <button
                class="absolute btn btn-circle btn-ghost top-1 right-1"
                @click="closeModal"
            >
                <svg
                    class="swap-on fill-current"
                    xmlns="http://www.w3.org/2000/svg"
                    width="32"
                    height="32"
                    viewBox="0 0 512 512"
                >
                    <polygon
                        points="400 145.49 366.51 112 256 222.51 145.49 112 112 145.49 222.51 256 112 366.51 145.49 400 256 289.49 366.51 400 400 366.51 289.49 256 400 145.49"
                    />
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, onMounted } from 'vue';
import apiClient from '@/api';
import { createPutRequest } from '@/functions/HttpRequest.js';
import { addAlert } from '@/functions/AlertManager';
import { loadImage } from '@/functions/Utils';
import ImageCarousel from './ImageCarousel.vue';
import PickerMapComponent from './PickerMapComponent.vue';
const MAX_IMAGE_COUNT = 10;
const MAX_IMAGES_SIZE = 100e6; // 100 MB

const BASE_URL = (() => {
    let url = process.env.VUE_APP_BASE_URL;
    if (url.endsWith('/')) {
        url = url.slice(0, -1);
    }
    return url;
})();

const props = defineProps({
    id: {
        type: String,
        required: true,
    },
    isOpen: {
        type: Boolean,
        required: true,
    },
});

const emit = defineEmits(['update-success', 'close']);

const activityName = ref('');
const activityDetail = ref('');
const date = ref('');
const endRegistrationDate = ref('');
const endDate = ref('');
const maxPeople = ref(0);
const people = ref([]);
const showMaxPeople = ref(false);
const images = ref([]);
const activity = ref({});
const new_images = ref([]);
const owner = ref(0);
const remove_attachment = ref([]);
const isDarkTheme = ref(false);
const showMinRep = ref(false)
const minRep = ref(0)

const fetchDetail = async () => {
    /**
     * Get data from specific activity including participant detail.
     * This function does not return anything.
     */
    try {
        const response = await apiClient.get(`/activities/${props.id}`);
        activity.value = response.data;
        // TEST DATA REMOVE AFTER API IS SENDING THE LOCATION DATA.
        activity.value['on_site'] = true; 
        activity.value['location'] = {
            lat: 13.84979,
            lon: 100.56836
        }
        //////////////////////////////////////////////////////////
        activityName.value = response.data.name || '';
        activityDetail.value = response.data.detail || '';
        date.value = formatActivityDate(new Date(response.data.date));
        endRegistrationDate.value = formatActivityDate(
            new Date(response.data.end_registration_date)
        );
        endDate.value = formatActivityDate(new Date(response.data.end_date));
        images.value = activity.value.images.map((image) => ({
            id: image.id,
            url: `${BASE_URL}${image.url}`,
        }));
        owner.value = response.data.owner;
        maxPeople.value = activity.value.max_people || activity.value.people;
        showMaxPeople.value = maxPeople.value > 1;
        people.value = activity.value.participant;
    } catch (error) {
        console.error('Error fetching activity:', error);
    }
};

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
    if (maxPeople.value < activity.value.people) {
        addAlert(
            'warning',
            'Max People must be higher or equal to current participants.'
        );
        maxPeople.value = activity.value.people;
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

    if (activity.value.on_site && !(activity.value.location.lat && activity.value.location.lon)) {
        addAlert(
            'warning',
            'Please Place the marker on the map.'
        )
        result = false;
    }

    return result;
};

const postUpdate = async () => {
    /*
     * Attempt to update activity information.
     * This function does not return anything.
     */

    if (!validateInput()) {
        return;
    }
    try {
        // Construct data to create POST request
        if (!showMaxPeople.value) {
            maxPeople.value = null;
        }
        new_images.value = images.value
            .filter((image) => image.id === -1)
            .map((image) => image.url);
        let data = {
            name: activityName.value,
            detail: activityDetail.value,
            date: date.value,
            end_registration_date: endRegistrationDate.value,
            end_date: endDate.value,
            max_people: maxPeople.value || null,
            new_images: new_images.value,
            remove_attachments: remove_attachment.value,
            owner: owner.value,
            minimum_reputation_score: minRep.value * 10
        };

        if (!activity.value.on_site) {
            data = {
                ...data,
                on_site: false,
            }
        } else {
            data = {
                ...data,
                on_site: true,
                location: {
                    lat: activity.value.location.lat,
                    lon: activity.value.location.lon
                }
            }
        }
        const response = await createPutRequest(
            `/activities/${props.id}/`,
            data
        );
        new_images.value = [];
        remove_attachment.value = [];
        addAlert('success', response.data.message);
        emit('update-success');
        await fetchDetail();
    } catch (error) {
        console.error(error);
        if (error.response && error.response.data) {
            addAlert('error', error.response.data.message); // Show error message from backend
        } else {
            addAlert(
                'error',
                'An unexpected error occurred. Please try again later.'
            );
        }
    }
};

const formatActivityDate = (date) => {
    /*
     * Adjust the activity date with the timezone offset.
     * Return localized time.
     */
    const dateObj = new Date(date);
    return dateObj;
};

const toggleMaxPeople = () => {
    /*
     * Toggle value of showMaxPeople.
     * Return nothing.
     */
    showMaxPeople.value = !showMaxPeople.value;
};

const toggleOnSite = () => {
    /*
     * Toggle value of showMaxPeople.
     * Return nothing.
     */
    activity.value.on_site = !activity.value.on_site;
};

const setMinRep = () => {
    /*
     * Switch the flag of setting minimum reputation.
     */
    showMinRep.value = !showMinRep.value;
};

const handleFileChange = (e) => {
    /*
     * Push value into images.
     * @params {image} image that uploads from input.
     * Return nothing.
     */
    const files = e.target.files;
    if (files.length > 0) {
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
                            (image) => image.url === imageSrc
                        );
                        if (!isDuplicate) {
                            images.value.push({ id: -1, url: imageSrc }); // Store the image source in the array
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
    }
};

const handleRemove = (index) => {
    /*
     * Remove image and push removed image id into array.
     * @params {int} image that wants to be removed.
     * Return nothing.
     */
    if (images.value[index].id != -1) {
        remove_attachment.value.push(images.value[index].id);
    }
    // Remove the image from the images array
    images.value.splice(index, 1);
    images.value = [...images.value];
};

const handleMarkerPlace = (coords) => {
    activity.value.location.lat = coords.lat;
    activity.value.location.lon = coords.lon; 
}

const maxImageCompute = () => {
    /*
     * Compute max image size.
     *
     * @returns {int} max image size in MB
     */
    return MAX_IMAGES_SIZE / 1e6;
};

const closeModal = () => {
    const modal = document.getElementById('edit-modal');
    modal.classList.add('opacity-0');
    setTimeout(() => {
        emit('close');
    }, 200);
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
    fetchDetail();
});
</script>
