<template>
    <div>
        <div class='breadcrumbs text-lm size-fit my-6 mx-10'>
            <ul>
                <li><a @click="goBack">Home</a></li>
                <li>Create Activity</li>
            </ul>
        </div>
        <div class='card p-6 bg-base-300 border-2 border-primary shadow-md rounded-lg m-6'>
            <div class='card-body p-4'>
                <h2 class='card-title text-2xl mr-2 text-base-content'>
                    Create Activity
                </h2>
                <div class="form-control w-full">
                    <div class="label"> 
                        <span class='text-base-content text-lg'> Activity Title </span>
                        <span id='name-field-error' class='text-error text-sm' hidden> required </span>
                    </div>
                    <input
                        v-model='activityName'
                        id='name-field'
                        type='text'
                        placeholder='Activity Title'
                        class='input input-bordered input-primary w-full mb-4'
                        :maxlength='255'
                        required
                    />
                </div>
                <div>
                        <label class="btn btn-primary">
                            Add Image
                            <input type="file" multiple 
                            id ='file-add'
                            accept="image/*"
                            @change="handleFileChange"
                            hidden
                            />
                        </label>
                </div>
                <div class="flex flex-col justify-center">
                    <div id='img-carousel' class='carousel w-full max-h-[50vh]' tabindex="-1" >
                        <div :id="'slide'+index" class="carousel-item relative w-full justify-center" v-for="(imageSrc, index) in images" :key="index">
                            <img
                                v-if="imageSrc"
                                v-lazy="imageSrc"
                            >
                            <div class="absolute left-5 right-5 top-1/2 flex -translate-y-1/2 transform justify-between">
                                <a @click.prevent="scrollCarousel(index - 1)" class="btn btn-circle">❮</a>
                                <a @click.prevent="scrollCarousel(index + 1)" class="btn btn-circle">❯</a>
                            </div>
                        </div>
                    </div>
                    <div class="flex w-full justify-center gap-2 py-2">
                        <a @click.prevent="scrollCarousel(index)" v-for="index in images.length" :key="index" class="btn btn-xs">{{index}}</a>

                    </div>
                </div>
                <div class="form-control w-full">
                    <div class="label">
                        <span class='text-base-content'> Activity Detail </span>
                        <span id='detail-field-error' class='text-error text-sm' hidden> required </span>
                    </div>
                    <textarea
                        v-model='activityDetail'
                        id='detail-field'
                        class='textarea textarea-primary w-full mb-4 resize-none'
                        placeholder='Activity Detail'
                        :maxlength='1024'
                        :rows="4"
                    >
                    </textarea>
                </div>
                <div class="form-control w-full">
                    <div class="label">
                        <span class='text-base-content'> Activity Date </span>
                        <span id='date-field-error' class='text-error text-sm' hidden> required </span>
                    </div>
                    <VueDatePicker
                        v-model='date'
                        id='date-field'
                        type='text'
                        placeholder='Select Date'
                        :min-date='new Date()'
                        :dark='isDarkTheme'
                    />
                </div>
                <label>Max People </label>
                <input type='checkbox' class='toggle' @change='setMaxPeople' />
                <input
                    v-if='showMaxPeople'
                    id='max-field'
                    v-model.number='maxPeople'
                    type='number'
                    placeholder='Enter Max People (Optional)'
                    class='input input-bordered input-primary w-full mb-4'
                    :min='1'
                />
                <div class="flex flex-col sm:flex-row justify-between">
                    <button v-if="!isAuth" class="btn btn-primary" @click="login">Please Login before create</button>
                    <button v-else class='btn btn-primary sm:my-0 my-6' @click='postCreateActivity'>
                        Create Activity
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { addAlert } from '@/functions/AlertManager';
import { createPostRequest } from '@/functions/HttpRequest';
import { isAuth, login } from '@/functions/Authentications';
import { loadImage } from '@/functions/Utils.';
</script>

<script>
export default {
    data() {
        return {
            activityName: '',
            activityDetail: '',
            date: '',
            maxPeople: 1,
            showMaxPeople: false,
            isDarkTheme: false,
            images: [],
        };
    },
    methods: {
        goBack() {
            /*
             * Navigate back to Activity Index page.
             */
            this.$router.push('/');
        },
        validateInput() { 
            /**
             * Validate input in the forms
             * @return input validity in boolean
             */
            var result = true;
            const nameField = document.getElementById('name-field')
            const nameFieldError = document.getElementById('name-field-error')
            if (this.activityName.length <= 0) {
                nameField.classList.remove('input-primary');
                nameField.classList.add('input-error');
                
                nameFieldError.removeAttribute('hidden');
                result = false;
            }
            else {
                nameFieldError.setAttribute('hidden', 'true');
                nameField.classList.remove('input-error');
                if (!nameField.classList.contains('textarea-primary'))
                    nameField.classList.add('textarea-primary');
            }
            const detailField = document.getElementById('detail-field')
            const detailFieldError = document.getElementById('detail-field-error')
            if (this.activityDetail.length <= 0) {
                detailField.classList.remove('textarea-primary');
                detailField.classList.add('input-error');
                
                detailFieldError.removeAttribute('hidden');
                result = false;
            }
            else {
                detailFieldError.setAttribute('hidden', 'true');
                detailField.classList.remove('input-error');
                if (!detailField.classList.contains('textarea-primary'))
                    detailField.classList.add('textarea-primary');
            }
            const dateFieldError = document.getElementById('date-field-error')
            if (this.date.length <= 0) {
                dateFieldError.removeAttribute('hidden');
                result = false;
            }
            else {
                dateFieldError.setAttribute('hidden', 'true')
            }
            if (this.maxPeople <= 0 && this.showMaxPeople) {
                addAlert('warning', 'Max People must be positive and not zeroes.')
                this.maxPeople = 1;
                result = false;
            }
            return result;
        },
        async postCreateActivity() {
            /*
             * Attempt to create activity.
             */
            if(!this.validateInput()) {
                return null;
            }
            try {
                // Construct data to create POST request
                const dateObj = new Date(this.date);
                const formattedDate = dateObj.toISOString();
                if (!this.showMaxPeople) {
                    this.maxPeople = null;
                }
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
                addAlert('success', response.data.message);
                this.$router.push(`/activities/${response.data.id}`);
            } catch (error) {
                if (error.response && error.response.data) {
                    addAlert('error', error.response.data.message); // Show error message from backend
                } else {
                    addAlert(
                        'error',
                        'An unexpected error occurred. Please try again later.'
                    );
                }
            }
        },
        setMaxPeople() {
            /*
             * Switch the flag of setting max people.
             */
            this.showMaxPeople = !this.showMaxPeople;
        },
        handleFileChange(event) {
            const files = event.target.files;
            if (files.length > 0) {
                Array.from(files).forEach(file => {
                loadImage(file)
                    .then(imageSrc => {
                        this.images.push(imageSrc); // Store the image source in the array
                    })
                    .catch(error => {
                        console.error('Error loading image:', error);
                    });
                });
            }
        },
        scrollCarousel(index) {
            const carousel = document.getElementById('img-carousel');

            let carouselW = carousel.clientWidth;
            let actualIndex = index < 0 ? this.images.length - 1 : index; 
            actualIndex = actualIndex >= this.images.length ? 0 : actualIndex;

            const targetPixel = (carouselW * actualIndex) + 1;
            carousel.scrollTo(targetPixel, 0);
        },
    },
    mounted() {
        this.isDarkTheme = window.matchMedia(
            '(prefers-color-scheme: dark)'
        ).matches;
        window
            .matchMedia('(prefers-color-scheme: dark)')
            .addEventListener('change', (e) => {
                this.isDarkTheme = e.matches;
            });
    },
};
</script>
