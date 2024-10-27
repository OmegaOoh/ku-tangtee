<template>
    <div>
        <div class="breadcrumbs text-lm size-fit my-6 mx-10 back">
            <ul>
                <li><a @click="goBack">Home</a></li>
                <li>Activity {{ activity.id }}</li>
            </ul>
        </div>
        <div
            class="modal backdrop-blur-sm"
            :class="{ 'modal-open': showModal }"
        >
            <div class="modal-box shadow-xl">
                <div class="sticky flex justify-end">
                    <button
                        class="btn btn-ghost btn-circle"
                        @click="closeModal"
                    >
                        x
                    </button>
                </div>
                <EditModal
                    @update-success="
                        () => {
                            this.closeModal();
                            this.fetchDetail();
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
                    {{ activity.name }}
                    <button
                        v-if="isHost"
                        @click="openModal"
                        class="btn btn-ghost text-accent ml-2 mr-2"
                    >
                        Edit
                    </button>
                </h1>
                <p class="mb-2 ml-3 overflow-hidden multi-line">
                    {{ activity.detail }}
                </p>
                <p class="mb-2 ml-3">
                    <strong class="text-base-content text-lg">Date:</strong>
                    {{ formatTimestamp(activity.date) }}
                </p>
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
                        class="card bg-base-100 shadow-lg p-4 rounded-lg"
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
import { format } from "date-fns";
import { addAlert } from "@/functions/AlertManager";
import apiClient from "@/api";
import {
    createDeleteRequest,
    createPostRequest,
} from "@/functions/HttpRequest.js";
import { isAuth, login, userId } from "@/functions/Authentications";
import { watch, ref } from "vue";
import EditModal from "@/component/EditModal.vue";
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
             */
            this.$router.push("/");
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
        goToChat() {
            /*
             * Navigagte to Activity Chart page.
             */
            this.$router.push(`/chat/${this.activityId}`);
        },
        async fetchDetail() {
            /*
             * Get data from specific activity including participant detail.
             */
            try {
                const response = await apiClient.get(
                    `/activities/${this.activityId}`
                );
                this.activity = response.data;
                this.people = this.activity.participant;
                this.canJoin = this.activity.can_join;
                this.hosts = JSON.stringify(response.data.host);
                this.checkHost();
                this.checkJoined();
            } catch (error) {
                console.error("Error fetching activity:", error);
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
                return format(new Date(timestamp), "PPp");
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
    },
    mounted() {
        this.activityId = this.$route.params.id;
        this.fetchDetail();
        this.checkHost();
        this.checkJoined();
        watch(userId, (newUserId) => {
            if (newUserId) {
                this.checkHost();
                this.checkJoined();
            }
        });
        watch(
            () => this.$route.params.id,
            (newId) => {
                this.activityId = newId;
                console.log("Fetch detail");
                this.fetchDetail();
            }
        );
        window.addEventListener("keydown", (e) => {
            if (e.key == "Escape") {
                this.closeModal();
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
