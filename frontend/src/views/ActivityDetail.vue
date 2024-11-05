<template>
    <div class="breadcrumbs text-lm size-fit my-6 mx-10 back">
        <ul>
            <li><a @click="goBack">Home</a></li>
            <li>Activity {{ activity.id }}</li>
        </ul>
    </div>
    <div v-if="isAuth && isHost">
        <EditModal 
            :id="activityId"
            :isOpen="showEditModal"
            @close="closeEditModal"
            @update-success="handleEditSuccess" />

        <CheckInCodeModal
            v-if="showCheckInCode"
            @closed-checked-in="handleCheckInClosed"
            @allow-checked-in="fetchDetail"
        />
    </div>
    <CheckInModal
        v-if="isAuth && isJoined && !isHost"
        :id="activityId"
        :isOpen="showCheckInModal"
        @close="closeCheckInModal"
        @check-in-success="handleCheckInSuccess"
    />
    

    <div class="card p-6 bg-base-300 border-2 border-primary shadow-md rounded-lg m-6">
        <div class="card-body p-4">
            <h1 class="text-4xl font-bold mb-4 ml-2 multi-line">
                {{ activity.name }}
                <button v-if="isHost && isAuth" @click="openEditModal" class="btn btn-ghost text-accent ml-2 mr-2">Edit</button>
                <button v-if="isHost && isAuth" @click="openCheckInCodeModal" class="btn btn-ghost text-accent ml-2 mr-2">
                    {{ activity.check_in_allowed ? 'Show Check-In Code' : 'Allow Check-in' }}
                </button>
                <button v-if="isJoined && isAuth && checkedIn && !isHost" class="btn btn-ghost text-accent ml-2 mr-2">You've Checked-In</button>
            </h1>

            <p class="mb-2 ml-3 overflow-hidden multi-line">{{ activity.detail }}</p>
            <p class="mb-2 ml-3"><strong>Date and Time:</strong> {{ formatTimestamp(activity.date) }}</p>

            <div v-if="imageUrls.length > 0" class="flex flex-col justify-center">
                <span class="text-base-content text-lg ml-3 mb-2">Preview Images</span>
                <ImageCarousel ref="imageCarousel" :images="imagesUrl" />
            </div>

            <p v-if="activity.max_people != null" class="mb-2 ml-3"><strong>Max People:</strong> {{ activity.max_people }}</p>
            <p class="mb-2 ml-3"><strong>Joined People:</strong></p>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-2 ml-3">
                <div
                    v-for="participant in people"
                    :key="participant.id"
                    class="card bg-base-100 shadow-lg p-4 rounded-lg border-primary hover:border-2 cursor-pointer transition-all duration-75 ease-in-out"
                    @click="$router.push('/profile/'+ participant.username)"
                >
                    <div class="flex items-center space-x-4">
                        <img
                            v-lazy="participant.profile_picture_url"
                            alt="Profile Picture"
                            class="w-12 h-12 rounded-full"
                            @error="handleImageError"
                        />
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
                        v-if="isJoined && activity.check_in_allowed && isAuth && !checkedIn"
                        @click="openCheckInModal"
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
</template>


<script setup>
import { ref, watch, onMounted, computed } from "vue";
import { format } from "date-fns";
import { addAlert } from "@/functions/AlertManager";
import apiClient from "@/api";
import {
    createDeleteRequest,
    createPostRequest,
} from "@/functions/HttpRequest.js";
import { isAuth, login, userId } from "@/functions/Authentications";
import EditModal from "@/component/EditModal.vue";
import ImageCarousel from "@/component/ImageCarousel";
import CheckInCodeModal from "@/component/CheckInCodeModal.vue";
import CheckInModal from "@/component/CheckInModal.vue";
import { useRoute, useRouter } from "vue-router";
const BASE_URL = (() => {
    let url = process.env.VUE_APP_BASE_URL
    if (url.endsWith("/")) {
        url = url.slice(0, -1);
    }
    return url;
})()

const router = useRouter();
const route = useRoute();

const activityId = ref(0)
const activity = ref({});
const imageUrls = ref([]);
const showEditModal = ref(false);
const showCheckInCode = ref(false);
const showCheckInModal = ref(false);
const people = ref([]);
const checkedIn = ref(false);
const canJoin = ref(true);
const hosts = ref([]);

const fetchDetail = async () => {
    try {
        const response = await apiClient.get(`/activities/${activityId.value}`);
        activity.value = response.data;
        people.value = activity.value.participant;
        imageUrls.value = activity.value.images.map(image => ({
            id: image.id,
            url: `${BASE_URL}${image.url}`
        }));
        canJoin.value = activity.value.can_join;
        hosts.value = response.data.host;
        checkCheckedIn();
    } catch (error) {
        console.error("Error fetching activity:", error);
        addAlert("warning", "Activity already started or No such activity.");
    }
};

const checkCheckedIn = () => {
    if (isAuth && isJoined.value) {
        const user = people.value.find(participant => participant.id === userId.value);
        checkedIn.value = user ? user.checked_in : false;
    } else {
        checkedIn.value = false;
    }
};

const formatTimestamp = (timestamp) => {
    return timestamp ? format(new Date(timestamp), "EEE, MMM/dd/yyyy, hh:mm a") : "No date provided";
};

const handleEditSuccess = async () => {
    await fetchDetail();
    closeEditModal();
};

const handleCheckInClosed = async () => {
    await fetchDetail();
    closeCheckInCodeModal();
};

const handleCheckInSuccess = async () => {
    await fetchDetail();
    closeCheckInModal();
};

const openEditModal = () => {
    showEditModal.value = true;
};

const closeEditModal = () => {
    showEditModal.value = false;
};

const openCheckInCodeModal = () => {
    showCheckInCode.value = true;
};

const closeCheckInCodeModal = () => {
    showCheckInCode.value = false;
};

const openCheckInModal = () => {
    showCheckInModal.value = true;
};

const closeCheckInModal = () => {
    showCheckInModal.value = false;
};

const goBack = () => {
    router.push("/");
};

const goToChat = () => {
    router.push(`/chat/${activityId.value}`);
};

const joinActivity = async () => {
    try {
        const response = await createPostRequest(`/activities/join/${activityId.value}/`, {});
        addAlert("success", response.data.message);
        await fetchDetail();
    } catch (error) {
        addAlert("error", error.response?.data?.message || "An unexpected error occurred. Please try again later.");
    }
};

const leaveActivity = async () => {
    try {
        const response = await createDeleteRequest(`/activities/join/${activityId.value}/`);
        addAlert("success", response.data.message);
        await fetchDetail();
    } catch (error) {
        addAlert("error", error.response?.data?.message || "An unexpected error occurred. Please try again later.");
    }
};

// Computed properties
const isHost = computed(() => {
    return isAuth && hosts.value.includes(userId.value);
});

const isJoined = computed(() => {
    return isAuth && people.value.some(participant => participant.id === userId.value);
});

const imagesUrl = computed(() => {
    console.log(imageUrls.value.map(image => image.url))
    return imageUrls.value.map(image => image.url)
})

onMounted(() => {
    activityId.value = route.params.id;
    fetchDetail();
    watch(() => route.params.id, (newId) => {
        activityId.value = newId;
        fetchDetail();
    });
    window.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
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