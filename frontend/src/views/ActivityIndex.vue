<template>
    <div class="fixed top-16 left-0 right-0 flex justify-center z-10" style="padding: 1%;">
        <div id="reload" class="transform translate-y-0 transition-transform duration-300 ease-in-out" hidden>
            <button class='btn btn-accent size-fit text-xl' @click='fetchActivities()'>
                ↻ Refresh
            </button>
        </div>
    </div>
    <div class='container mx-auto p-4'>
        <h1 class='text-4xl font-bold mb-4 flex justify-center'>Activities List</h1>
        <div v-if='activities.length'>
            <div class='grid grid-cols-1 md:grid-cols-2 gap-4'>
                <div
                    v-for='activity in activities'
                    :key='activity.id'
                    class='card bg-base-300 hover:border-primary border-2 border-base-300 shadow-lg transition-all duration-150'
                >
                    <div
                        class='card-body p-4 '
                        style='border-radius: 8px'
                    >
                        <h2 class='card-title text-2xl font-semibold overflow-hidden whitespace-nowrap text-ellipsis'>
                            {{ activity.name }}
                        </h2>
                        <p class='line-clamp-2 text-ellipsis'>{{ activity.detail }}</p>
                        <p>
                            Start date:
                            {{ formatActivityDate(activity.date) }}
                        </p>
                        <div class='card-actions justify-end'>
                            <router-link
                                :to='{ path: `/activities/${activity.id}` }'
                            >
                                <button
                                    class='btn btn-secondary'
                                    @click='viewActivity(activity.id)'
                                >
                                    View
                                </button>
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-else class='mt-4'>
            <div class="card bg-base-300 border-2 border-accent p-5">
                <div class="card-title text-2xl font-semibold">
                    No upcoming activities found.
                </div>
                <div class='card-actions justify-end'>
                    <router-link to='/create'>
                        <button class="btn btn-accent">Create New!</button>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import apiClient from '@/api'; // Get API
import '@/styles/ActivityIndex.css';

export default {
    data() {
        return {
            activities: [],
            isDarkTheme: false,
            timeZoneOffset: 0,
        };
    },
    mounted() {
        this.fetchTimeZoneOffset();
        this.fetchActivities();
        this.setupSocket();
        this.isDarkTheme = window.matchMedia(
            '(prefers-color-scheme: dark)'
        ).matches;
        window
            .matchMedia('(prefers-color-scheme: dark)')
            .addEventListener('change', (e) => {
                this.isDarkTheme = e.matches;
            });
    },
    methods: {
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
        async fetchActivities() {
            /*
             * Get data for all activities from API.
             */
            try {
                const response = await apiClient.get('/activities/'); // Trying to get data from API
                this.activities = response.data;
                window.scrollTo(0,0);
                // Hide reload button
                const reloadButton = document.getElementById('reload')
                reloadButton.classList.remove('translate-y-0');
                reloadButton.classList.remove('translate-y-[100%]');
                setTimeout(reloadButton.setAttribute('hidden', 'true'));

            } catch (error) {
                console.error('Error fetching activities:', error);
                if (error.response) {
                    console.error('Response data:', error.response.data);
                    console.error('Response status:', error.response.status);
                }
            }
        },
        viewActivity(activityId) {
            /*
             * Navigate to specific activity detail page.
             */
            this.$router.push(`/activities/${activityId}`);
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
        setupSocket() {
            /*
             * Connect to websocket to observe the change of index.
             * Return Nothing
             */
            const socket = new WebSocket(`${process.env.VUE_APP_BASE_URL.replace(/^http/, 'ws')
                                                                        .replace(/^https/, 'wss')}ws/index/`);

            socket.onmessage = (event) => {
                    try {
                        var parsedData = JSON.parse(event.data);
                        if (parsedData['type'] === 'new_act') {
                                // Show reload button
                                const reloadButton = document.getElementById('reload');
                                reloadButton.removeAttribute('hidden'); // Show the button
                                reloadButton.classList.remove('translate-y-[-100%]'); // Remove off-screen class
                                reloadButton.classList.add('translate-y-0'); // Slide in
                        }
                    } catch (error) {
                        console.log('Parsing Error: ', error)
                    }
            }        
        }
    },
};
</script>

<style scoped>
    .line-clamp-2 {
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;
        line-clamp: 2;
        word-wrap: normal;
        overflow: hidden;
    }
</style>