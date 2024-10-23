
<template>
    <div
        class="modal"
        :class="{ 'modal-open': showModal }">
        <div class="modal-box border-2 border-primary">
            <div class="sticky flex justify-end">
                <button
                    class="btn btn-ghost btn-circle"
                    @click="closeModal">
                    x
                </button>
            </div>
            <EditModal @update-success="closeModal"/>
        </div>
    </div>
    <div class='card p-6 bg-base-300 border-2 border-primary shadow-md rounded-lg m-6'>
        <div class='card-body p-4' style='border-radius: 8px'>
            <h1 class='text-4xl font-bold mb-4 ml-2'>
                {{ activity.name }}
                <button v-if="isHost" @click="openModal" class='btn btn-ghost ml-2 mr-2'>
                        Edit
                </button>
            </h1>
            <p class='mb-2 ml-3 overflow-hidden'>
                <strong class='text-lg'>Details:</strong> {{ activity.detail }}
            </p>
            <p class='mb-2 ml-3'>
                <strong class='text-lg'>Date:</strong>
                {{ formatActivityDate(activity.date) }}
            </p>
            <p class='mb-2 ml-3'>
                <strong class='text-lg'>Max People:</strong>
                {{ activity.max_people }}
            </p>
            <p class='mb-2 ml-3'>
                <strong class='text-lg'>Joined People:</strong>
            </p>
            <div class='grid grid-cols-1 md:grid-cols-3 gap-4 mb-2 ml-3'>
                <div
                    v-for='participant in people'
                    :key='participant.id'
                    class='card bg-base-100 shadow-lg p-4 rounded-lg'
                >
                    <div class='flex items-center space-x-4'>
                        <img
                            v-lazy='participant.profile_picture_url'
                            alt='Profile Picture'
                            class='w-12 h-12 rounded-full'
                            @error="handleImageError"
                        />
                        <p class='font-medium'>
                            {{ participant.first_name }}
                            {{ participant.last_name }}
                        </p>
                    </div>
                </div>
            </div>

            <div class='flex flex-col sm:flex-row justify-between items-center'>
                <div class='sm: my-5'>
                    <button @click='goBack' class='btn btn-info mx-2'>
                        Back to Activities
                    </button>
                </div>
                <div v-if="!isAuth">
                    <button class="btn btn-accent" @click="login">Please Login before join</button>
                </div>
                <div v-else-if="isJoined" class='flex'>
                    <button class="btn btn-secondary">
                        Chat
                    </button>
                    <button v-if='!isHost' class="btn btn-accent mx-4">
                        Leave Activity
                    </button>
                </div>
                <div v-else>
                    <button v-if="canJoin"
                        id="join-button"
                        @click='joinActivity'
                        class='btn btn-primary ml-2 mr-2'
                    >
                        Join Activity
                    </button>
                    <button v-else
                        id="join-button"
                        @click='joinActivity'
                        class='btn btn-disabled ml-2 mr-2'
                    >
                        Join Activity
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { addAlert } from '@/functions/AlertManager';
import apiClient from '@/api';
import { createPostRequest } from '@/functions/HttpRequest.js';
import { isAuth, login, userId } from '@/functions/Authentications';
import { watch, ref } from 'vue';
import EditModal from '@/component/EditModal.vue';
</script>

<script>

export default {
    data() {
        return {
            activity: {},
            canJoin: true,
            activityId: null,
            isDarkTheme: false,
            timeZoneOffset: 0,
            people: [],
            hosts: [],
            isHost: false,
            isJoined: false,
            showModal: ref(false),
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
        openModal() {
            /**
             * Show Edit Activity Modal
             * This function return nothing.
             */
            this.showModal = true;
        },
        closeModal() {
            /**
             * Close Edit Activity Modal
             * This function return nothing.
             */
             this.showModal = false;
        },
        async fetchTimeZoneOffset() {
            /*
             * Attempt to get timezone offset.
             * This function does not return anything.
             */
            try {
                const response = await apiClient.get(
                    'activities/get-timezone/'
                );
                this.timeZoneOffset = response.data.offset; // Set the time zone offset
            } catch (error) {
                console.error('Error fetching time zone offset:', error);
            }
        },
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
                this.people = participant.data;
                this.canJoin = this.activity.can_join;
                this.hosts = response.data.host;
                this.checkHost();
                this.checkJoined();
            } catch (error) {
                console.error('Error fetching activity:', error);
            }
        },
        async joinActivity() {
            /*
             * Attempt to join activity.
             * This function does not return anything.
             */
            try {
                const response = await createPostRequest(
                    `/activities/${this.activityId}/`,
                    {}
                );
                addAlert('success', response.data.message);
                this.fetchDetail(); //Fetch Activity
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
        formatActivityDate(date) {
            /*
             * Adjust the activity date with the timezone offset.
             * Return localized time.
             */
            const dateObj = new Date(date);
            const offsetMilliseconds = this.timeZoneOffset * 60 * 60 * 1000;
            const localDate = new Date(dateObj.getTime() + offsetMilliseconds);
            return localDate.toLocaleString(); // Return the localized date string
        },
        checkJoined() {
            /**
             * Check if current user joined the activity
             * return boolean whether or not user is joined
             */
            this.isJoined = this.people.some(element => element['id'] === userId.value);
        },
        checkHost() {
            /**
             * Check whether or not user is host of activity.
             * return boolean
             */
            this.isHost = this.hosts.includes(userId.value);
        },
        handleImageError(event) {
            console.error(event);
        }
    },
    mounted() {
        this.activityId = this.$route.params.id;
        this.fetchDetail();
        this.isDarkTheme = window.matchMedia(
            '(prefers-color-scheme: dark)'
        ).matches;
        window
            .matchMedia('(prefers-color-scheme: dark)')
            .addEventListener('change', (e) => {
                this.isDarkTheme = e.matches;
            });
        this.fetchTimeZoneOffset();
        watch(userId, (newUserId) => {
            if(newUserId) {
                this.checkHost();
                this.checkJoined();
            }
        })
        window.addEventListener('keydown', (e) => {
            if (e.key == 'Escape') {
                this.closeModal();
            }
        })
    },
};

</script>
