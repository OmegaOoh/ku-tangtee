<template>
    <div class="h-[100vh] overflow-x-hidden" @scroll.passive="handleScroll">
        <div
            class="fixed top-16 left-0 right-0 flex justify-center z-10"
            style="padding: 1%"
        >
            <div
                id="reload"
                class="translate-y-[-100%] transition-all duration-300 ease-in-out transform-gpu"
                hidden
            >
                <button class="btn btn-accent size-fit text-xl" @click="reload">
                    ↻ Refresh
                </button>
            </div>
        </div>
        <h1 class="text-4xl font-bold mb-4 flex justify-center my-6">
            Activities List
        </h1>

        <div class="container mx-auto p-4">
            <div class="grid grid-flow-col justify-end pr-5 items-center">
                <div class="flex my-5">
                    <input
                        v-model="searchKeyword"
                        @keydown.enter="fetchActivities(1, true)"
                        class="input input-bordered gap-2 rounded-r-none"
                        placeholder="Search"
                    />
                    <div>
                        <div class="relative">
                            <button
                                @click="toggleFilter"
                                class="btn btn-primary rounded-none"
                            >
                                filter
                            </button>
                            <div
                                v-if="isFilterOpen"
                                class="right-0 absolute dropdown-content bg-base-200 rounded-box w-fit z-[1] p-4 shadow"
                            >
                                <VueDatePicker
                                    v-model="dateRange"
                                    id="date-field"
                                    type="text"
                                    placeholder="Filter by date range"
                                    :min-date="null"
                                    :max-date="null"
                                    :dark="isDarkTheme"
                                    range
                                    :partial-range="false"
                                    class="mb-3"
                                />
                                <div class="flex flex-row justify-between">
                                    <label
                                        class="cursor-pointer flex flex-col items-center mr-3"
                                    >
                                        <input
                                            type="checkbox"
                                            class="checkbox"
                                            value="1"
                                            :checked="isChecked(1)"
                                            @change="toggleDay(1)"
                                        />
                                        <span>Su</span>
                                    </label>
                                    <label
                                        class="cursor-pointer flex flex-col items-center mr-3"
                                    >
                                        <input
                                            type="checkbox"
                                            class="checkbox"
                                            value="2"
                                            :checked="isChecked(2)"
                                            @change="toggleDay(2)"
                                        />
                                        <span>Mo</span>
                                    </label>
                                    <label
                                        class="cursor-pointer flex flex-col items-center mr-3"
                                    >
                                        <input
                                            type="checkbox"
                                            class="checkbox"
                                            value="3"
                                            :checked="isChecked(3)"
                                            @change="toggleDay(3)"
                                        />
                                        <span>Tu</span>
                                    </label>
                                    <label
                                        class="cursor-pointer flex flex-col items-center mr-3"
                                    >
                                        <input
                                            type="checkbox"
                                            class="checkbox"
                                            value="4"
                                            :checked="isChecked(4)"
                                            @change="toggleDay(4)"
                                        />
                                        <span>We</span>
                                    </label>
                                    <label
                                        class="cursor-pointer flex flex-col items-center mr-3"
                                    >
                                        <input
                                            type="checkbox"
                                            class="checkbox"
                                            value="5"
                                            :checked="isChecked(5)"
                                            @change="toggleDay(5)"
                                        />
                                        <span>Th</span>
                                    </label>
                                    <label
                                        class="cursor-pointer flex flex-col items-center mr-3"
                                    >
                                        <input
                                            type="checkbox"
                                            class="checkbox"
                                            value="6"
                                            :checked="isChecked(6)"
                                            @change="toggleDay(6)"
                                        />
                                        <span>Fr</span>
                                    </label>
                                    <label
                                        class="cursor-pointer flex flex-col items-center mr-3"
                                    >
                                        <input
                                            type="checkbox"
                                            class="checkbox"
                                            value="7"
                                            :checked="isChecked(7)"
                                            @change="toggleDay(7)"
                                        />
                                        <span>Sa</span>
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button
                        @click="fetchActivities(1, true)"
                        class="btn btn-secondary rounded-l-none"
                    >
                        Search
                    </button>
                </div>
            </div>
            <div v-if="activities.length">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div
                        v-for="activity in activities"
                        :key="activity.id"
                        class="card bg-base-300 hover:border-primary border-2 border-base-300 shadow-lg transition-all duration-150"
                    >
                        <div class="card-body p-4" style="border-radius: 8px">
                            <h2
                                class="card-title text-2xl font-semibold line-clamp-1"
                            >
                                {{ activity.name }}
                            </h2>
                            <p>
                                <strong>Close Registration: </strong>
                                {{
                                    formatTimestamp(
                                        activity.end_registration_date
                                    )
                                }}
                            </p>

                            <span class="mb-2">
                                <strong> Activity Period: </strong>
                                <span
                                    v-if="
                                        formatDate(activity.date) !=
                                        formatDate(activity.end_date)
                                    "
                                >
                                    {{ formatTimestamp(activity.date) }} -
                                    {{ formatTimestamp(activity.end_date) }}
                                </span>
                                <span v-else>
                                    {{ formatDate(activity.date) }},
                                    {{ formatTime(activity.date) }} -
                                    {{ formatTime(activity.end_date) }}
                                </span>
                            </span>

                            <div
                                v-if="
                                    activity.minimum_reputation_score != null &&
                                    calcMinRep(
                                        activity.minimum_reputation_score
                                    ) > 0
                                "
                                class="absolute top-2 right-2 badge badge-accent p-3"
                            >
                                lvl >
                                {{
                                    calcMinRep(
                                        activity.minimum_reputation_score
                                    )
                                }}
                            </div>

                            <div class="card-actions justify-end">
                                <router-link
                                    :to="{ path: `/activities/${activity.id}` }"
                                >
                                    <button
                                        class="btn btn-secondary"
                                        @click="viewActivity(activity.id)"
                                    >
                                        View
                                    </button>
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else class="mt-4">
                <div class="card bg-base-300 border-2 border-accent p-5">
                    <div class="card-title text-2xl font-semibold">
                        No upcoming activities found.
                    </div>
                    <div class="card-actions justify-end">
                        <router-link to="/create">
                            <button class="btn btn-accent">Create New!</button>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { format } from 'date-fns';
import apiClient from '@/api';

const router = useRouter();

// Variable
const activities = ref([]);
const isDarkTheme = ref(false);
const searchKeyword = ref('');
const socket = ref(null);
const startDate = ref(null);
const endDate = ref(null);
const dateRange = ref(null);
const selectedDay = ref([1, 2, 3, 4, 5, 6, 7]);
const isFilterOpen = ref(false);
const currentPage = ref(1);
const isLoading = ref(false);
const noNextPage = ref(false);

/**
 * Fetch Data
 */
const fetchActivities = async (page = 1, reset = false) => {
    /*
     * Get data for all activities from API.
     */
    if (isLoading.value) return;
    isLoading.value = true;

    try {
        let response;
        const params = { page: page };

        // Add parameters only if they have values
        if (searchKeyword.value) {
            params.keyword = searchKeyword.value;
        }
        if (startDate.value) {
            params.start_date = format(startDate.value, 'yyyy-MM-dd');
        }
        if (endDate.value) {
            params.end_date = format(endDate.value, 'yyyy-MM-dd');
        }
        if (selectedDay.value) {
            params.day = selectedDay.value.toString();
        }
        response = await apiClient.get('/activities/', { params });
        if (reset) {
            activities.value = [];
            noNextPage.value = false;
            currentPage.value = 1;
        }
        activities.value.push(...response.data.results);
        noNextPage.value = response.data.next == null;
    } catch (error) {
        console.error('Error fetching activities:', error);
        if (error.response) {
            console.error('Response data:', error.response.data);
            console.error('Response status:', error.response.status);
        }
    } finally {
        isLoading.value = false;
    }
};

const reload = () => {
    fetchActivities(1, true);
    const reloadButton = document.getElementById('reload');
    if (reloadButton) {
        if (!reloadButton.hasAttribute('hidden'))
            setTimeout(reloadButton.setAttribute('hidden', ''), 300);
        reloadButton.classList.remove('translate-y-0');
        reloadButton.classList.add('translate-y-[-100%]');
    }
};

const handleScroll = ({
    target: { scrollTop, clientHeight, scrollHeight },
}) => {
    if (
        scrollTop + clientHeight >= scrollHeight - 100 &&
        !isLoading.value &&
        !noNextPage.value
    ) {
        currentPage.value++;
        fetchActivities(currentPage.value);
    }
};

/**
 * Redirect
 */

const viewActivity = (activityId) => {
    /*
     * Navigate to specific activity detail page.
     */
    router.push(`/activities/${activityId}`);
};

/**
 * Websocket
 */

const setupSocket = () => {
    /*
     * Connect to websocket to observe the change of index.
     */
    const new_socket = new WebSocket(
        `${process.env.VUE_APP_BASE_URL.replace(/^http/, 'ws').replace(
            /^https/,
            'wss'
        )}ws/index/`
    );
    socket.value = new_socket;

    socket.value.onmessage = (event) => {
        try {
            var parsedData = JSON.parse(event.data);
            if (parsedData['type'] === 'new_act') {
                // Show reload button
                const reloadButton = document.getElementById('reload');
                if (reloadButton) {
                    reloadButton.removeAttribute('hidden');
                    reloadButton.classList.remove('translate-y-[-100%]');
                    reloadButton.classList.add('translate-y-0');
                }
            }
        } catch (error) {
            console.error('Parsing Error: ', error);
        } finally {
            isLoading.value = false;
        }
    };
};

/**
 * Utils
 */

const toggleFilter = () => {
    /**
     * Function to toggle filter dropdown status
     */
    isFilterOpen.value = !isFilterOpen.value;
};

const toggleDay = (value) => {
    /**
     * Toggle value inside selectedDay array
     */
    value = Number(value);
    const index = selectedDay.value.indexOf(value);
    if (index === -1) {
        selectedDay.value.push(value);
    } else {
        selectedDay.value.splice(index, 1);
    }
};

const isChecked = (value) => {
    /**
     * Check if the selectedDays is include the value.
     * @return boolean
     */
    return selectedDay.value.includes(Number(value));
};

const calcMinRep = (minRepScore) => {
    return Math.floor(minRepScore / 10);
};

const formatTimestamp = (timestamp) => {
    /*
     * Format the timestamp into (Oct 22, 2024, 9:00 AM).
     *
     * @params {string} not yet formatted timestamp
     * @returns {string} formatted timestamp
     */
    return `${formatDate(timestamp)}, ${formatTime(timestamp)}`;
};

const formatDate = (timestamp) => {
    return timestamp
        ? format(new Date(timestamp), 'EEE, MMM/dd/yyyy')
        : 'No date provided';
};

const formatTime = (timestamp) => {
    return timestamp
        ? format(new Date(timestamp), 'hh:mm a')
        : 'No time provided';
};

onMounted(() => {
    fetchActivities();
    setupSocket();
    isDarkTheme.value = window.matchMedia(
        '(prefers-color-scheme: dark)'
    ).matches;
    window
        .matchMedia('(prefers-color-scheme: dark)')
        .addEventListener('change', (e) => {
            isDarkTheme.value = e.matches;
        });
});

onBeforeUnmount(() => {
    if (socket.value) socket.value.close();
});
</script>

<style scoped>
.line-clamp-2 {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    word-wrap: break-word;
    overflow: hidden;
    text-overflow: ellipsis;
}

.line-clamp-1 {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 1;
    line-clamp: 1;
    word-wrap: break-word;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
