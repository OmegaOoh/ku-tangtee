<template>
    <div class="h-[100vh] overflow-x-hidden">
        <div class="breadcrumbs text-lm size-fit my-6 mx-10 overflow-visible">
            <ul>
                <li><a @click="goBack">Home</a></li>
                <li>Activity {{ activity.id }}</li>
            </ul>
        </div>
        <div v-if="isAuth && isHost && !isCancelled && isBeforeEndDate">
            <EditModal
                :id="activityId"
                :isOpen="showEditModal"
                @close="
                    () => {
                        showEditModal = false;
                    }
                "
                @update-success="handleEditSuccess"
            />

            <CheckInCodeModal
                v-if="showCheckInCode"
                :id="activityId"
                :isOpen="showCheckInCode"
                @close="closeCheckInCodeModal"
            />

            <EditPermModal
                :id="activityId"
                :isOpen="showEditPermModal"
                @close="
                    () => {
                        showEditPermModal = false;
                    }
                "
                @update-success="handleEditPermSuccess"
            />

            <CheckInQRCodeModal
                :id="activityId"
                :isOpen="showQRCode"
                @close="
                    () => {
                        showQRCode = false;
                    }
                "
            />
        </div>
        <CheckInModal
            v-if="
                isAuth && isJoined && !isHost && !isCancelled && isBeforeEndDate
            "
            :id="activityId"
            :isOpen="showCheckInModal"
            @close="
                () => {
                    showCheckInModal = false;
                }
            "
            @check-in-success="handleCheckInSuccess"
        />

        <div
            class="card p-6 bg-base-300 border-2 border-primary shadow-md rounded-lg m-6"
        >
            <div class="card-body p-4">
                <h1 class="text-4xl font-bold mb-4 ml-2 multi-line">
                    <span> {{ activity.name }} </span>
                    <span
                        v-if="isJoined && isAuth && checkedIn && !isHost"
                        class="text-xl text-primary"
                    >
                        ✓
                    </span>
                </h1>

                <!--Owner action set-->
                <div
                    v-if="isHost && isAuth && !isCancelled && isBeforeEndDate"
                    class="flex-auto"
                >
                    <button
                        @click="
                            () => {
                                showEditModal = true;
                            }
                        "
                        class="btn btn-ghost text-accent ml-2 mr-2"
                    >
                        Edit
                    </button>
                    <button
                        v-if="isOwner"
                        @click="
                            () => {
                                showEditPermModal = true;
                            }
                        "
                        class="btn btn-ghost text-accent mx-2"
                    >
                        Manage participants
                    </button>
                    <button
                        v-if="activity.check_in_allowed"
                        @click="
                            () => {
                                showCheckInCode = true;
                            }
                        "
                        class="btn btn-ghost text-accent ml-2 mr-2"
                    >
                        Show Check-In Code
                    </button>

                    <button
                        v-if="activity.check_in_allowed"
                        @click="
                            () => {
                                showQRCode = true;
                            }
                        "
                        class="btn btn-ghost text-accent ml-2 mr-2"
                    >
                        QR Code
                    </button>

                    <button
                        v-else
                        @click="allowCheckIn"
                        class="btn btn-ghost text-accent ml-2 mr-2"
                    >
                        Allow Check-in
                    </button>
                </div>

                <div
                    v-if="imageUrls.length > 0"
                    class="flex flex-col justify-center"
                >
                    <span class="text-base-content text-lg ml-3 mb-2"
                        >Images</span
                    >
                    <ImageCarousel
                        ref="imageCarousel"
                        carouselName="detail-carousel"
                        :images="imagesUrl"
                    />
                </div>

                <div
                    class="mb-2 ml-3 overflow-hidden multi-line"
                    v-html="markdownFormatter(activity.detail)"
                ></div>

                <div class="ml-3" v-if="activity.on_site">
                    <strong class="text-base-content text-lg mt-2 mb-4"
                        >Location</strong
                    >
                    <div v-if="showMap">
                        <MapComponent
                            :latitude="activity.location.lat"
                            :longitude="activity.location.lon"
                            class="h-[30vh] w-[100%] ml-2 rounded-lg overflow-hidden z-0"
                        />
                    </div>
                    <div
                        v-else
                        class="skeleton h-[30vh] w-[100%] ml-2 rounded-lg overflow-hidden"
                    ></div>
                </div>

                <p class="mt-2 ml-3">
                    <strong class="text-base-content text-lg"
                        >Close Registration:</strong
                    >
                    {{ formatTimestamp(activity.end_registration_date) }}
                </p>

                <span class="mb-2 ml-3">
                    <strong class="text-lg"> Activity Period: </strong>
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
                        minRepLv > 0
                    "
                    class="absolute top-2 left-2 badge badge-accent p-3"
                >
                    lvl > {{ minRepLv }}
                </div>

                <span class="mb-2 ml-3"
                    ><strong>Joined People: </strong>
                    <div class="badge badge-secondary">
                        {{ activity.people }}
                        <div v-if="activity.max_people != null" class="ml-1">
                            /
                        </div>
                        <div v-if="activity.max_people != null" class="ml-1">
                            {{ activity.max_people }}
                        </div>
                    </div>
                </span>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-2 ml-3">
                    <div
                        v-for="participant in people"
                        :key="participant.user.id"
                        class="card bg-base-100 shadow-lg p-4 rounded-lg hover:border-primary border-2 border-base-300 cursor-pointer transition-all duration-75 ease-in-out"
                        @click="
                            $router.push(
                                '/profile/' + participant.user.username
                            )
                        "
                    >
                        <div class="flex items-center space-x-4">
                            <div class="indicator">
                                <img
                                    v-lazy="
                                        participant.user.user_profile
                                            .profile_picture_url
                                    "
                                    alt="Profile Picture"
                                    class="w-12 h-12 rounded-full"
                                    @error="handleImageError"
                                />
                                <p
                                    v-if="hosts.includes(participant.user.id)"
                                    class="indicator-item indicator-bottom indicator-center badge badge-secondary"
                                >
                                    Host
                                </p>
                            </div>
                            <p class="font-medium">
                                {{ participant.user.first_name }}
                                {{ participant.user.last_name }}
                            </p>
                        </div>
                    </div>
                </div>
                <div class="mx-auto">
                    <button
                        class="btn btn-sm btn-neutral mr-4"
                        @click="fetchParticipant(1)"
                    >
                        first
                    </button>
                    <button
                        class="btn btm-sm rounded-r-none"
                        :class="havePage(havePrev)"
                        @click="fetchParticipant(currentPage - 1)"
                    >
                        prev
                    </button>
                    <button class="btn btm-sm rounded-none">
                        Page {{ currentPage }}
                    </button>
                    <button
                        class="btn btm-sm rounded-l-none"
                        :class="havePage(haveNext)"
                        @click="fetchParticipant(currentPage + 1)"
                    >
                        next
                    </button>
                    <button
                        class="btn btn-sm btn-neutral ml-4"
                        @click="fetchParticipant(lastPage)"
                    >
                        last
                    </button>
                </div>
                <div class="ml-4">
                    <div v-if="!isAuth">
                        <button class="btn btn-accent" @click="login">
                            Please Login before join
                        </button>
                    </div>
                    <div
                        v-else-if="isJoined"
                        class="flex justify-between w-full"
                    >
                        <div class="flex flex-row">
                            <button class="btn btn-secondary" @click="goToChat">
                                Chat
                            </button>
                            <button
                                v-if="
                                    isJoined &&
                                    activity.check_in_allowed &&
                                    isAuth &&
                                    !checkedIn &&
                                    !isHost
                                "
                                @click="
                                    () => {
                                        showCheckInModal = true;
                                    }
                                "
                                class="btn btn-secondary mx-4"
                            >
                                Check-In
                            </button>
                        </div>

                        <button
                            v-if="!isHost"
                            @click="leaveActivity"
                            class="btn btn-accent mx-4"
                            :class="
                                checkDatePassed(activity.end_registration_date)
                                    ? 'btn-disabled disabled'
                                    : 'btn-accent'
                            "
                        >
                            Leave Activity
                        </button>
                    </div>
                    <div v-else>
                        <button
                            v-if="
                                !activity.is_full &&
                                activity.is_active &&
                                !isJoined &&
                                !isHost
                            "
                            id="join-button"
                            @click="joinActivity"
                            class="btn btn-primary ml-2 mr-2"
                        >
                            Join Activity
                        </button>
                        <button
                            v-else
                            id="join-button"
                            @click="joinActivity"
                            class="btn btn-disabled ml-2 mr-2"
                        >
                            Join Activity
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue';
import { format } from 'date-fns';
import { addAlert } from '@/functions/AlertManager';
import apiClient from '@/api';
import {
    createDeleteRequest,
    createPostRequest,
    createPutRequest,
} from '@/functions/HttpRequest.js';
import { isAuth, login, userId } from '@/functions/Authentications';
import EditModal from '@/component/EditModal.vue';
import EditPermModal from '@/component/EditPermModal.vue';
import ImageCarousel from '@/component/ImageCarousel';
import CheckInCodeModal from '@/component/CheckInCodeModal.vue';
import CheckInModal from '@/component/CheckInModal.vue';
import CheckInQRCodeModal from '@/component/CheckInQRCodeModal.vue';
import { useRoute, useRouter } from 'vue-router';
import { markdownFormatter } from '@/functions/Utils';
import MapComponent from '@/component/MapComponent.vue';

const BASE_URL = (() => {
    let url = process.env.VUE_APP_BASE_URL;
    if (url.endsWith('/')) {
        url = url.slice(0, -1);
    }
    return url;
})();

const router = useRouter();
const route = useRoute();

const activityId = ref(0);
const activity = ref({});
const imageUrls = ref([]);
const showEditModal = ref(false);
const showEditPermModal = ref(false);
const showCheckInCode = ref(false);
const showCheckInModal = ref(false);
const showQRCode = ref(false);
const people = ref([]);
const checkedIn = ref(false);
const hosts = ref([]);
const owner = ref(0);
const minRepLv = ref(0);
const isJoined = ref(false);
const isCancelled = ref(false);

// Participant Pagination
const PAGINATION_SIZE = 20;
const currentPage = ref(1);
const havePrev = ref(false);
const haveNext = ref(true);
let participantCount = 0;

const showMap = computed(() => {
    return (
        !showEditModal.value &&
        !showCheckInCode.value &&
        !showQRCode.value &&
        !showCheckInModal.value &&
        !showEditPermModal.value
    );
});

const fetchDetail = async () => {
    try {
        const response = await apiClient.get(`/activities/${activityId.value}`);
        activity.value = response.data;
        fetchParticipant();
        imageUrls.value = activity.value.images.map((image) => ({
            id: image.id,
            url: `${BASE_URL}${image.url}`,
        }));
        hosts.value = response.data.host;
        owner.value = response.data.owner;
        minRepLv.value = Math.floor(
            response.data.minimum_reputation_score / 10
        );
        isCancelled.value = response.data.is_cancelled;
        checkCheckedIn();
        fetchIsJoined();
    } catch (error) {
        console.error('Error fetching activity:', error);
        addAlert('warning', 'Activity already started or No such activity.');
    }
};

const fetchIsJoined = async () => {
    const response = await apiClient.get(
        `/activities/${activityId.value}/is-joined/`
    );
    isJoined.value = response.data.is_joined;
};

const fetchParticipant = async (page = 1) => {
    const params = { page: page };
    const response = await apiClient.get(
        `/activities/participant/${activityId.value}/`,
        { params }
    );
    console.log("Fetch participant here")
    console.log(response.data.results)
    people.value = response.data.results;
    participantCount = response.data.count;
    haveNext.value = response.data.next != null;
    havePrev.value = response.data.previous != null;
};

const havePage = (havePage) => {
    if (havePage) return 'btn-neutral';
    return 'btn-disabled';
};

const allowCheckIn = async () => {
    /*
     * Attempt to join activity.
     */
    try {
        const response = await createPutRequest(
            `/activities/check-in/${activityId.value}/?status=open`,
            {}
        );
        addAlert('success', response.data.message);
        showCheckInCode.value = true;
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

const checkCheckedIn = () => {
    console.log("check check-in here")
    console.log(people.value)
    if (isAuth && isJoined.value) {
        const user = people.value.find(
            (participant) => participant.user.id === userId.value
        );
        checkedIn.value = user ? user.checked_in : false;
    } else {
        checkedIn.value = false;
    }
};

const checkDatePassed = (timestamp) => {
    const checkDate = new Date(timestamp);
    const today = new Date();
    return checkDate < today;
};

const formatTimestamp = (timestamp) => {
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

const handleEditSuccess = async () => {
    await fetchDetail();
    closeEditModal();
};

const handleEditPermSuccess = async () => {
    await fetchDetail();
    closeEditPermModal();
};

const handleCheckInSuccess = async () => {
    await fetchDetail();
    showCheckInModal.value = false;
};

const closeEditModal = () => {
    showEditModal.value = false;
};
true;

const closeEditPermModal = () => {
    showEditPermModal.value = false;
};
true;

const closeCheckInCodeModal = (allowed) => {
    activity.value.check_in_allowed = allowed;
    showCheckInCode.value = false;
};

const goBack = () => {
    router.push('/');
};

const goToChat = () => {
    router.push(`/chat/${activityId.value}`);
};

const joinActivity = async () => {
    try {
        const response = await createPostRequest(
            `/activities/join/${activityId.value}/`,
            {}
        );
        addAlert('success', response.data.message);
        await fetchDetail();
    } catch (error) {
        addAlert(
            'error',
            error.response?.data?.message ||
                'An unexpected error occurred. Please try again later.'
        );
    }
};

const leaveActivity = async () => {
    try {
        const response = await createDeleteRequest(
            `/activities/join/${activityId.value}/`
        );
        addAlert('success', response.data.message);
        await fetchDetail();
    } catch (error) {
        addAlert(
            'error',
            error.response?.data?.message ||
                'An unexpected error occurred. Please try again later.'
        );
    }
};

// Computed properties
const isHost = computed(() => {
    return isAuth && hosts.value.includes(userId.value);
});

const isOwner = computed(() => {
    return userId.value === owner.value;
});

const lastPage = computed(() => {
    return Math.ceil(participantCount / PAGINATION_SIZE);
});

const isBeforeEndDate = computed(() => {
    const currentDate = new Date();
    const endDate = new Date(activity.value.end_date);
    return currentDate < endDate;
});

const imagesUrl = computed(() => {
    return imageUrls.value.map((image) => image.url);
});

watch(
    () => route.params.id,
    (newId) => {
        activityId.value = newId;
        fetchDetail();
    }
);

watch(userId, (newUserId) => {
    if (newUserId) {
        fetchIsJoined();
        checkCheckedIn();
    }
});

onMounted(() => {
    activityId.value = route.params.id;
    fetchDetail();

    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeEditModal();
        }
    });
});
</script>

<style scoped>
.multi-line {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    word-wrap: break-word;
}
</style>
