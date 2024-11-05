<template>
    <div>
        <div class="breadcrumbs text-lm size-fit my-6 mx-10 back">
            <ul>
                <li><a @click="goBack">Home</a></li>
                <li>Activity {{ activity.id }}</li>
            </ul>
        </div>
        <div v-if="isHost && isAuth">
            <div
            class="modal backdrop-blur-sm"
            :class="{ 'modal-open': showEditModal }"
            >
                <div class="modal-box shadow-xl">
                    <div class="sticky flex justify-end">
                        <button
                            class="btn btn-ghost btn-circle absolute hover:text-error"
                            @click="closeEditModal"
                        >
                            <svg
                                class="swap-on fill-current"
                                xmlns="http://www.w3.org/2000/svg"
                                width="32"
                                height="32"
                                viewBox="0 0 512 512">
                                <polygon
                                points="400 145.49 366.51 112 256 222.51 145.49 112 112 145.49 222.51 256 112 366.51 145.49 400 256 289.49 366.51 400 400 366.51 289.49 256 400 145.49" />
                            </svg>
                        </button>
                    </div>
                    <EditModal
                        @update-success="
                            async () => {
                                await fetchDetail();
                                closeEditModal();
                            }
                        "
                    />
                </div>
            </div>
        
            <div
                class="modal backdrop-blur-sm"
                :class="{ 'modal-open': showCheckInCode }"
            >
                <div class="modal-box shadow-xl">
                    <button
                        class="btn btn-ghost btn-circle absolute right-6 top-6 hover:text-error"
                        @click="closeCheckInCodeModal"
                    >
                        <svg
                            class="swap-on fill-current"
                            xmlns="http://www.w3.org/2000/svg"
                            width="32"
                            height="32"
                            viewBox="0 0 512 512">
                            <polygon
                            points="400 145.49 366.51 112 256 222.51 145.49 112 112 145.49 222.51 256 112 366.51 145.49 400 256 289.49 366.51 400 400 366.51 289.49 256 400 145.49" />
                        </svg>
                    </button>
                    <CheckInCodeModal
                        @closed-checked-in = "
                            async () => {
                                this.closeCheckInCodeModal();
                                await this.fetchDetail();
                            }
                        "
                        @allow-checked-in = "
                            async () => {
                                await this.fetchDetail();
                            }
                        "
                    />
                </div>
            </div>
            <CheckInQRCodeModal :code="getCheckInCode()" :is-open="showQRModal" @close="() => {showQRModal = false;}"/>
        </div>
        <div
            class="modal backdrop-blur-sm"
            :class="{ 'modal-open': showCheckInModal }"
        >
            <div class="modal-box shadow-xl">
                <div class="sticky flex justify-end">
                    <button
                        class="btn btn-ghost btn-circle absolute right-2 top-2 hover:text-error"
                        @click="closeCheckInModal"
                    >
                    <svg
                        class="swap-on fill-current"
                        xmlns="http://www.w3.org/2000/svg"
                        width="32"
                        height="32"
                        viewBox="0 0 512 512">
                        <polygon
                        points="400 145.49 366.51 112 256 222.51 145.49 112 112 145.49 222.51 256 112 366.51 145.49 400 256 289.49 366.51 400 400 366.51 289.49 256 400 145.49" />
                    </svg>
                </button>
                </div>
                <CheckInModal
                    @check-in-success = "
                        async () => {
                            this.closeCheckInModal();
                            await this.fetchDetail();
                        }
                    "
                />
            </div>
        </div>
        <div
            class="card p-6 bg-base-300 border-2 border-primary shadow-md rounded-lg m-6"
        >
            <div class="card-body p-4" style="border-radius: 8px">
                <h1 class="text-4xl font-bold mb-4 ml-2 multi-line">
                    <span>
                        {{ activity.name }}
                        <button
                            v-if="isHost && isAuth"
                            @click="openEditModal"
                            class="btn btn-ghost text-accent mx-2"
                        >
                            Edit
                        </button>
                        <button
                            v-if="isHost && isAuth"
                            @click="openCheckInCodeModal"
                            class="btn btn-ghost text-accent mx-2"
                        >
                            <div v-if="!activity.check_in_allowed">
                                Allow Check-in
                            </div>
                            <div v-else>
                                Show Check-In Code
                            </div>
                        </button>
                        <button
                            v-if="isHost && isAuth && activity.check_in_allowed"
                            class="btn btn-ghost text-accent mx-2"
                            @click="() => { showQRModal = true; console.log(activity.check_in_code)}"
                            >
                            QR CODE
                        </button>
                    </span> 
                    <span
                            v-if="isJoined && isAuth && checkedIn && !isHost"
                            class="text-sm text-accent mx-2"
                        >
                            Checked-In
                    </span>
                </h1>
                <p class="mb-2 ml-3 overflow-hidden multi-line">
                    {{ activity.detail }}
                </p>
                <p class="mb-2 ml-3">
                    <strong class="text-base-content text-lg">Date and Time:</strong>
                    {{ formatTimestamp(activity.date) }}
                </p>
                <div
                    v-if="imageUrls.length > 0"
                    class="flex flex-col justify-center"
                >
                    <span class="text-base-content text-lg ml-3 mb-2">
                        Preview Images
                    </span>
                    <ImageCarousel
                        ref="imageCarousel"
                        carouselName="detail-carousel"
                        :images="imageUrls.map((image) => image.url)"
                    />
                </div>
                <p v-if="activity.max_people != null" class="mb-2 ml-3">
                    <strong class="text-base-content text-lg"
                        >Max People:</strong
                    >
                    {{ activity.max_people }}
                </p>
                <p class="mb-2 ml-3">
                    <strong class="text-base-content text-lg"
                        >Joined People:</strong
                    >
                </p>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-2 ml-3">
                    <div
                        v-for="participant in people"
                        :key="participant.id"
                        class="card bg-base-100 shadow-lg p-4 rounded-lg border-primary hover:border-2 cursor-pointer transition-all duration-75 ease-in-out"
                        @click="$router.push('/profile/'+ participant.username)"
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
                                    v-if="this.hosts.includes(participant.id)" 
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
                    class="flex flex-col md:flex-row items-center justify-between"
                >
                    <div v-if="!isAuth">
                        <button class="btn btn-accent" @click="login">
                            Please Login before join
                        </button>
                    </div>
                    <div v-else-if="isJoined" class="w-full flex">
                        <div class="flex w-1/2 justify-start">
                            <button class="btn btn-secondary " @click="goToChat">
                                Chat
                            </button>
                            <button
                                v-if="isJoined && activity.check_in_allowed && isAuth && !checkedIn"
                                @click="openCheckInModal"
                                class="btn btn-secondary mx-4 "
                            >
                                Check-In
                            </button>
                        </div>
                        <div class="flex justify-end w-full">
                            <button
                                v-if="!isHost"
                                @click="leaveActivity"
                                class="btn btn-accent mx-4"
                            >
                                Leave Activity
                            </button>
                        </div>
                    </div>
                    <div v-else>
                        <button
                            v-if="canJoin"
                            id="join-button"
                            @click="joinActivity"
                            class="btn btn-primary "
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
import { format } from "date-fns";
import { addAlert } from "@/functions/AlertManager";
import apiClient from "@/api";
import {
    createDeleteRequest,
    createPostRequest,
} from "@/functions/HttpRequest.js";
import { isAuth, login, userId } from "@/functions/Authentications";
import { watch } from "vue";
import EditModal from "@/component/EditModal.vue";
import ImageCarousel from "@/component/ImageCarousel";
import CheckInCodeModal from "@/component/CheckInCodeModal.vue";
import CheckInModal from "@/component/CheckInModal.vue";
import CheckInQRCodeModal from "@/component/CheckInQRCodeModal.vue";

</script>

<script>
export default {
    components: {
        ImageCarousel,
    },
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
            showEditModal: false,
            showCheckInCode: false,
            showCheckInModal: false,
            showQRModal: false,
            checkedIn: false,
            baseUrl: "",
            images: [],
            imageUrls: [],
        };
    },
    methods: {
        goBack() {
            /*
             * Navigate back to Activity Index page.
             */
            this.$router.push("/");
        },
        openEditModal() {
            /**
             * Show Edit Activity Modal
             * This function return nothing.
             */
            this.showEditModal = true;
        },
        closeEditModal() {
            /**
             * Close Edit Activity Modal
             * This function return nothing.
             */
            this.showEditModal = false;
        },
        openCheckInCodeModal() {
            /**
             * Open Activity checkin code
             */
            this.showCheckInCode = true;
        },
        closeCheckInCodeModal() {
            /**
             * Open Activity checkin code
             */
            this.showCheckInCode = false;
        },
        openCheckInModal() {
            /**
             * Open participant check-in modal
             */
            this.showCheckInModal = true;
        },
        closeCheckInModal() {
            /**
             * Close participant check-in modal
             */
            this.showCheckInModal = false;
        },
        goToChat() {
            /*
             * Navigate to Activity Chart page.
             */
            this.$router.push(`/chat/${this.activityId}`);
        },
        async fetchDetail() {
            /*
             * Get data from specific activity including participant detail.
             */
            try {
                if (!this.activityId) {
                    return // undefined activity id, return early
                }
                const response = await apiClient.get(
                    `/activities/${this.activityId}`
                );
                this.activity = response.data;
                this.people = this.activity.participant;
                console.log(this.people)
                this.images = this.activity.images;
                this.imageUrls = [];
                this.baseUrl = process.env.VUE_APP_BASE_URL;
                if (this.baseUrl.endsWith("/")) {
                    this.baseUrl = this.baseUrl.slice(0, -1);
                }
                for (const image of this.images) {
                    const imageurl = this.baseUrl + image.url;
                    this.imageUrls.push({ id: image.id, url: imageurl });
                }
                if (this.$refs.imageCarousel) {
                    this.$refs.imageCarousel.images = this.imageUrls.map(
                        (image) => image.url
                    );
                }
                this.canJoin = this.activity.can_join;
                this.hosts = JSON.stringify(response.data.host);
                this.checkHost();
                this.checkJoined();
                this.checkCheckedIn();
            } catch (error) {
                console.error("Error fetching activity:", error);
                addAlert(
                    "warning",
                    "Activity already started or No such activity."
                );
            }
        },
        async joinActivity() {
            /*
             * Attempt to join activity.
             */
            try {
                const response = await createPostRequest(
                    `/activities/join/${this.activityId}/`,
                    {}
                );
                addAlert("success", response.data.message);
                this.fetchDetail(); //Fetch Activity
            } catch (error) {
                if (error.response && error.response.data) {
                    addAlert("error", error.response.data.message); // Show error message from backend
                } else {
                    addAlert(
                        "error",
                        "An unexpected error occurred. Please try again later."
                    );
                }
            }
        },
        async leaveActivity() {
            /**
             * Attempt Leave activity
             * this function return nothing
             */
            try {
                const response = await createDeleteRequest(
                    `/activities/join/${this.activityId}/`
                );
                addAlert("success", response.data.message);
                this.fetchDetail(); //Fetch Activity
            } catch (error) {
                if (error.response && error.response.data) {
                    addAlert("error", error.response.data.message); // Show error message from backend
                } else {
                    addAlert(
                        "error",
                        "An unexpected error occurred. Please try again later."
                    );
                }
            }
        },
        formatTimestamp(timestamp) {
            /*
             * Format the timestamp into (Oct 22, 2024, 9:00 AM).
             *
             * @params {string} not yet formatted timestamp
             * @returns {string} formatted timestamp
             */
            if (timestamp) {
                return format(new Date(timestamp), "EEE, MMM/dd/yyyy, hh:mm a");
            } else {
                return "No date provided";
            }
        },
        checkJoined() {
            /**
             * Check if current user joined the activity
             * return None
             */
            if (!isAuth) {
                this.isJoined = false;
            } else {
                this.isJoined = this.people.some(
                    (element) => element["id"] == userId.value
                );
            }
        },
        checkHost() {
            /**
             * Check whether or not user is host of activity.
             * return None
             */
            if (!isAuth) {
                this.isHost = false;
            } else {
                this.isHost = this.hosts.includes(userId.value);
            }
        },
        getCheckInCode() {
            /**
             * Get Current Check In code
             * @returns string of check in code
             */
            if (!isAuth || !this.isHost) {
                return "None" // No permission to see
            }
            return this.activity.check_in_code;
        },
        checkCheckedIn() {
            /**
             * Check whether or not user is host of activity.
             * return None
             */
            if (!isAuth || !this.isJoined) {
                this.checkedIn = false;
            } else {
                const user = this.people.filter(
                    (element) => element["id"] == userId.value
                );
                this.checkedIn = user[0].checked_in
            }
        },
        checkDefaultCode() {
            const code = this.$route.query.code;
            console.log(isAuth.value, this.isJoined, !this.checkCheckedIn, code)
            if (isAuth.value && this.isJoined && !this.checkedIn && code) {
                console.log("checkDefault Code", code)
                this.openCheckInModal();
            }
        }
    },
    async mounted() {
        this.activityId = this.$route.params.id;
        await this.fetchDetail();
        this.checkHost();
        this.checkJoined();
        this.checkCheckedIn();
        this.checkDefaultCode();

        watch(userId, (newUserId) => {
            if (newUserId) {
                this.checkHost();
                this.checkJoined();
                this.checkCheckedIn();
                this.checkDefaultCode();
            }
        });
        watch(
            () => this.$route.params.id,
            (newId) => {
                this.activityId = newId;
                this.fetchDetail();
            }
        );
        window.addEventListener("keydown", (e) => {
            if (e.key == "Escape") {
                this.closeEditModal();
            }
        });
    },
};
</script>

<style scoped>
.multi-line {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    word-wrap: break-word;
}
</style>
