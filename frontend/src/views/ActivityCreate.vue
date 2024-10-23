<template>
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
            <div class="form-control w-full">
                <div class="label">
                    <span class='text-base-content'> Activity Detail </span>
                    <span id='detail-field-error' class='text-error text-sm' hidden> required </span>
                </div>
                <textarea
                    v-model='activityDetail'
                    id='detail-field'
                    class='textarea textarea-primary w-full mb-4'
                    placeholder='Activity Detail'
                    :maxlength='1024'
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
                <button class='btn btn-primary' @click='goBack'>
                    Back to List
                </button>
                <button v-if="!isAuth" class="btn btn-accent" @click="login">Please Login before create</button>
                <button v-else class='btn btn-accent sm:my-0 my-6' @click='postCreateActivity'>
                Create Activity
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { addAlert } from '@/functions/AlertManager';
import { createPostRequest } from '@/functions/HttpRequest';
import { isAuth, login } from '@/functions/Authentications';
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
        };
    },
    methods: {
        goBack() {
            /*
             * Navigate back to Activity Index page.
             * This function does not return anything.
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
            if (this.maxPeople <= 0) {
                addAlert('warning', 'Max People must be positive and not zeroes.')
                this.maxPeople = 1;
                result = false;
            }
            return result;
        },
        async postCreateActivity() {
            /*
             * Attempt to create activity.
             * This function does not return anything.
             */
            if(!this.validateInput()) {
                return null;
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
            this.showMaxPeople = !this.showMaxPeople;
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
