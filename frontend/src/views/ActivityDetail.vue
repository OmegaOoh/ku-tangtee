<template>
    <div class="overflow-x-hidden">
        <div class="breadcrumbs text-lm size-fit my-6 mx-10 overflow-visible">
            <ul>
                <li><a @click="goBack">Home</a></li>
                <li>Activity {{ activity.id }}</li>
            </ul>
        </div>
        <div v-if="isAuth && isHost">
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
            v-if="isAuth && isJoined && !isHost"
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
                <div v-if="isHost && isAuth" class="flex-auto">
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

                <p class="mb-2 ml-3 overflow-hidden multi-line">
                    {{ activity.detail }}
                </p>
                <p class="mb-2 ml-3">
                    <strong class="text-base-content text-lg"
                        >Start Date and Time:</strong
                    >
                    {{ formatTimestamp(activity.date) }}
                </p>
                <p class="mb-2 ml-3">
                    <strong class="text-base-content text-lg"
                        >End Registration Date:</strong
                    >
                    {{ formatTimestamp(activity.end_registration_date) }}
                </p>
                <p class="mb-2 ml-3">
                    <strong class="text-base-content text-lg"
                        >End Date and Time:</strong
                    >
                    {{ formatTimestamp(activity.end_date) }}
                </p>
                <div
                    v-if="imageUrls.length > 0"
                    class="flex flex-col justify-center"
                >
                    <span class="text-base-content text-lg ml-3 mb-2"
                        >Preview Images</span
                    >
                    <ImageCarousel
                        ref="imageCarousel"
                        carouselName="detail-carousel"
                        :images="imagesUrl"
                    />
                </div>

                <p v-if="activity.max_people != null" class="mb-2 ml-3">
                    <strong>Max People:</strong> {{ activity.max_people }}
                </p>
                <p class="mb-2 ml-3"><strong>Joined People:</strong></p>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-2 ml-3">
                    <div
                        v-for="participant in people"
                        :key="participant.id"
                        class="card bg-base-100 shadow-lg p-4 rounded-lg border-primary hover:border-2 cursor-pointer transition-all duration-75 ease-in-out"
                        @click="
                            $router.push('/profile/' + participant.username)
                        "
                    >
                        <div class="flex items-center space-x-4">
                            <div class="indicator">
                                <img
                                    v-lazy="participant.profile_picture_url"
                                    alt="Profile Picture"
                                    class="w-12 h-12 rounded-full"
                                    @error="handleImageError"
                                />
                                <p
                                    v-if="hosts.includes(participant.id)"
                                    class="indicator-item indicator-bottom indicator-center badge badge-secondary"
                                >
                                    Host
                                </p>
                            </div>
                            <p class="font-medium">
                                {{ participant.first_name }}
                                {{ participant.last_name }}
                            </p>
                        </div>
                    </div>
                </div>
                <div
                    class="flex flex-col sm:flex-row justify-between items-center"
                >
                    <div v-if="!isAuth">
                        <button class="btn btn-accent" @click="login">
                            Please Login before join
                        </button>
                    </div>
                    <div v-else-if="isJoined" class="flex">
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
                        <button
                            v-if="!isHost"
                            @click="leaveActivity"
                            class="btn btn-accent mx-4"
                        >
                            Leave Activity
                        </button>
                    </div>
                    <div v-else>
                        <button
                            v-if="canJoin"
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
const canJoin = ref(true);
const hosts = ref([]);
const owner = ref(0);

const fetchDetail = async () => {
    try {
        const response = await apiClient.get(`/activities/${activityId.value}`);
        activity.value = response.data;
        people.value = activity.value.participant;
        imageUrls.value = activity.value.images.map((image) => ({
            id: image.id,
            url: `${BASE_URL}${image.url}`,
        }));
        canJoin.value = activity.value.can_join;
        hosts.value = response.data.host;
        owner.value = response.data.owner;
        checkCheckedIn();
    } catch (error) {
        console.error('Error fetching activity:', error);
        addAlert('warning', 'Activity already started or No such activity.');
    }
};

async function allowCheckIn() {
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
}

const checkCheckedIn = () => {
    if (isAuth && isJoined.value) {
        const user = people.value.find(
            (participant) => participant.id === userId.value
        );
        checkedIn.value = user ? user.checked_in : false;
    } else {
        checkedIn.value = false;
    }
};

const formatTimestamp = (timestamp) => {
    return timestamp
        ? format(new Date(timestamp), 'EEE, MMM/dd/yyyy, hh:mm a')
        : 'No date provided';
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

const isJoined = computed(() => {
    return (
        isAuth &&
        people.value.some((participant) => participant.id === userId.value)
    );
});

const imagesUrl = computed(() => {
    return imageUrls.value.map((image) => image.url);
});

onMounted(() => {
    activityId.value = route.params.id;
    fetchDetail();
    watch(
        () => route.params.id,
        (newId) => {
            activityId.value = newId;
            fetchDetail();
        }
    );
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
