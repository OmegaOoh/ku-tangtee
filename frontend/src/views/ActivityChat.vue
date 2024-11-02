<template>
    <div class="w-screen overflow-x-hidden">
        <div class="breadcrumbs text-lm size-fit ml-10 my-6">
            <ul>
                <li><a @click="goHome">Home</a></li>
                <li>
                    <a @click="goDetail">Activity {{ activityId }}</a>
                </li>
                <li>Chat</li>
            </ul>
        </div>
        <div
            v-if="isAuth & isJoined"
            class="card bg-base-300 mx-10 border-2 border-primary"
        >
            <div class="relative flex flex-col h-[65vh]">
                <ul
                    ref="messageList"
                    class="card-body overflow-y-auto h-[70vh] break-words -z-10"
                    @scroll="handleScroll"
                >
                    <li v-for="(message, index) in messages" :key="index">
                        <div
                            :class="[
                                'chat',
                                Number(message.user_id) === currentUserId
                                    ? 'chat-end'
                                    : 'chat-start',
                            ]"
                        >
                            <div class="chat-image avatar">
                                <div class="w-10 rounded-full">
                                    <img
                                        alt="No Profile Picture"
                                        v-lazy="
                                            getProfilePicture(
                                                (userId = message.user_id)
                                            )
                                        "
                                    />
                                </div>
                            </div>
                            <div class="chat-header">
                                {{ getFullName(message.user_id) }}
                                <time class="text-xs opacity-50">{{
                                    formatTimestamp(message.timestamp)
                                }}</time>
                            </div>
                            <div class="chat-bubble chat-bubble-primary">
                                <div
                                    v-html="formatMessage(message.message)"
                                ></div>
                                <div
                                    v-if="
                                        message.images &&
                                        message.images.length > 0
                                    "
                                    class="image-grid mt-2"
                                >
                                    <ImageGrid
                                        componentSize="h-[15vh] w-[15vh]"
                                        :images="
                                            message.images.map(
                                                (image) => baseUrl + image
                                            )
                                        "
                                    />
                                </div>
                            </div>
                        </div>
                    </li>
                </ul>
                <div class="border-t-2 border-base-100 pt-2">
                    <div
                        v-if="images.length > 0"
                        class="min-h-10 max-h-[15vh] mx-4 bottom-1 mb-2"
                    >
                        <ImageGrid
                            componentSize="h-[15vh] w-1/12"
                            :images="images"
                            :removable="true"
                            @onRemove="(index) => images.splice(index, 1)"
                        />
                    </div>
                    <div class="flex justify-between items-center my-3 mx-3">
                        <div
                            class="flex justify-start textarea textarea-primary w-full py-0 px-2 overflow-hidden pt-0.5"
                        >
                            <label
                                class="text-base-content hover:text-primary transition-colors ease-in-out pb-1 text-3xl"
                            >
                                +
                                <input
                                    type="file"
                                    multiple
                                    id="file-add"
                                    accept="image/*"
                                    @change="handleFileChange"
                                    hidden
                                />
                            </label>
                            <textarea
                                v-model="newMessage"
                                placeholder="Start your chat"
                                class="resize-none size-full bg-inherit focus:outline-none align-middle pt-1.5 px-2"
                                :maxlength="1024"
                                @keydown.exact.enter.prevent="sendMessage"
                                @keydown.shift.enter.prevent="insertNewLine"
                                rows="1"
                            ></textarea>
                        </div>

                        <button
                            class="btn btn-primary mx-2"
                            @click="sendMessage"
                        >
                            Send
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div
            v-else-if="isAuth & !isJoined"
            class="card bg-base-300 mx-10 border-2 border-accent"
        >
            <div class="card-body">
                <h2 class="card-title">
                    The chat is exclusive to participants.
                </h2>
                <div class="card-actions justify-end">
                    <button
                        @click="goDetail"
                        class="card-action btn btn-accent"
                    >
                        To Detail
                    </button>
                </div>
            </div>
        </div>
        <div v-else class="card bg-base-300 mx-10 border-2 border-warning">
            <div class="card-body">
                <h2 class="card-title">Please Login before continue.</h2>
                <div class="card-actions justify-end">
                    <button @click="login" class="card-action btn btn-accent">
                        Login
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import apiClient from "@/api";
import { format } from "date-fns";
import  { watch } from 'vue'
import { login, isAuth, userId as authUserId } from "@/functions/Authentications";
import { addAlert } from "@/functions/AlertManager";
import { loadImage } from "@/functions/Utils.";
import ImageGrid from "@/component/ImageGrid.vue";
</script>

<script>
const MAX_IMAGE_COUNT = 5;
const MAX_IMAGES_SIZE = 50e6; // 50 MB

export default {
    data() {
        return {
            socket: null,
            newMessage: "",
            messages: [],
            activityId: this.$route.params.id,
            people: [],
            currentUserId: null,
            isJoined: false,
            isAtBottom: true,
            images: [],
            baseUrl: "",
        };
    },
    methods: {
        connectWebSocket() {
            /*
             * Connect to websocket to observe the change of index.
             * Return Nothing
             */
            const socket = new WebSocket(
                `${process.env.VUE_APP_BASE_URL.replace(/^http/, "ws").replace(
                    /^https/,
                    "wss"
                )}ws/chat/${this.activityId}`
            );
            this.socket = socket;
            this.socket.onopen = () => {
                console.log("WebSocket connection opened", this.activityId);
            };
            this.socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                const user_id = data.user_id;
                if (data.message) {
                    this.messages.push({
                        message: data.message,
                        timestamp: new Date(),
                        user_id: user_id,
                        images: data.images,
                    });
                    this.scrollToBottom();
                    if (
                        !this.people.some((element) => element.id === user_id)
                    ) {
                        this.fetchSingleProfile(user_id);
                    }
                }
            };
            this.socket.onclose = () => {
                console.log("WebSocket connection closed");
            };
            this.socket.onerror = (error) => {
                console.error("WebSocket error: ", error);
            };
        },
        sendMessage() {
            /*
             * Send message using text in text area.
             * Return Nothing
             */
            let trimMessage = this.newMessage.trim();
            if (trimMessage === "") {
                return;
            }
            if (this.socket.readyState === WebSocket.OPEN) {
                this.socket.send(
                    JSON.stringify({
                        message: trimMessage,
                        user_id: authUserId.value,
                        images: this.images,
                    })
                );
                this.images = [];
                this.newMessage = "";
            } else {
                console.log("WebSocket is not open.");
            }
        },
        insertNewLine() {
            /*
             * Add one line to the message.
             * Return Nothing
             */
            this.newMessage += "\n";
        },
        async fetchCurrentUser() {
            /*
             * Get current user that is on the current browser tab.
             * Return Nothing
             */
            this.currentUserId = authUserId.value;
        },
        async fetchProfile() {
            /*
             * Get attendee profiles.
             * Return Nothing
             */
            this.people = [];
            const response = await apiClient.get(
                `/activities/${this.activityId}/`
            );
            const activity = response.data;
            this.people = activity.participant;
        },
        async fetchSingleProfile(userId) {
            /*
             * Get single attendee profile.
             * Return Nothing
             */
            const uid = Number(userId);
            const participant = await apiClient.get(`/get-user/${uid}/`);
            this.people.push(participant.data);
        },
        async fetchMessages() {
            /*
             * Get all previous messages.
             * Return Nothing
             */
            this.messages = [];
            try {
                const response = await apiClient.get(
                    `/chat/${this.activityId}/`
                );
                this.messages = response.data;
                this.baseUrl = process.env.VUE_APP_BASE_URL;
                if (this.baseUrl.endsWith("/")) {
                    this.baseUrl = this.baseUrl.slice(0, -1);
                }
                this.scrollToBottom();
            } catch (error) {
                console.error("Error fetching messages:", error);
            }
        },
        scrollToBottom() {
            /*
             * Scroll the page to the bottom.
             * Return Nothing
             */
            this.$nextTick(() => {
                const messageList = this.$refs.messageList;
                if (messageList) {
                    if (this.isAtBottom){
                        messageList.scrollTo(0,messageList.scrollHeight);
                        this.scrollButtonVisibility(false);}
                    else {
                        this.scrollButtonVisibility(true);
                    }
                }
            });
        },
        scrollButtonVisibility(visibility) {
            /**
             * Handle Opacity of scrollButton
             * this function return nothing
             */
            const button = document.getElementById('bottom-button')
            if (visibility)
            {
                button.classList.remove('opacity-0')
            }
            else if (!button.classList.contains('opacity-0')) {
                button.classList.add('opacity-0');
            }


        },
        handleScroll() {
            /**
             * Handle Scrolling events in message list.
             * This function return nothing.
             */
            const messageList = this.$refs.messageList;
            if (!messageList) { 
                return; //messageList is null return early
            }
            const scrollTop = messageList.scrollTop;
            const clientHeight = messageList.clientHeight;
            const scrollHeight = messageList.scrollHeight;

            // Check if the user is at the bottom
            this.isAtBottom = scrollTop + clientHeight >= scrollHeight - 10;
        },
        formatTimestamp(timestamp) {
            /*
             * Format the timestamp into (Oct 22, 2024, 9:00 AM).
             *
             * @params {string} not yet formatted timestamp
             * @returns {string} formatted timestamp
             */
            return format(new Date(timestamp), "PPp");
        },
        formatMessage(message) {
            /*
             * Format message to be html format with <br> instead of \n.
             *
             * @params {string} not yet formatted message
             * @returns {string} formatted message
             */
            return message.replace(/\n/g, "<br>");
        },
        getProfilePicture(userId) {
            /*
             * Get profile picture from specific user id.
             *
             * @params {Number} sender user id
             * @returns {string} profile picture url
             */
            const participant = this.people.find(
                (person) => person.id === Number(userId)
            );
            return participant ? participant.profile_picture_url : null;
        },
        getFullName(userId) {
            /*
             * Get user fullname from specific user id.
             *
             * @params {Number} sender user id
             * @returns {string} user firstname and lastname
             */
            const participant = this.people.find(
                (person) => person.id === Number(userId)
            );
            return participant
                ? `${participant.first_name} ${participant.last_name}`
                : "Unknown User";
        },
        goHome() {
            /**
             * Navigate back to index page
             * @returns Nothing
             */
            this.$router.push(`/`);
        },
        goDetail() {
            /**
             * Navigate user back to activity page.
             * @returns Nothing
             */
            this.$router.push(`/activities/${this.activityId}`);
        },
        checkJoined() {
            /**
             * Check if current user joined the activity
             * return boolean whether or not user is joined
             */
            this.isJoined = this.people.some(
                (element) => element["id"] == authUserId.value
            );
        },
        async chatSetup() {
            await this.fetchProfile();
            await this.checkJoined();
            if (this.isJoined) {
                if (this.socket) {
                    this.socket.close();
                    this.connectWebSocket();
                }
                await this.fetchCurrentUser();
                await this.fetchMessages();
            }
        },
        handleFileChange(event) {
            /*
             * Push value into images.
             * @params {image} image that uploads from input.
             * Return nothing.
             */
            const files = event.target.files;
            if (files.length > 0) {
                // Check total image count
                if (files.length + this.images.length > MAX_IMAGE_COUNT) {
                    addAlert(
                        "warning",
                        "You can add at most " + MAX_IMAGE_COUNT + " pictures"
                    );
                    return;
                }

                // Calculate total size of current and new images
                let totalSize = this.images.reduce(
                    (sum, file) => sum + file.size,
                    0
                );

                Array.from(files).forEach((file) => {
                    totalSize += file.size;
                });

                // Check if total size exceeds limit
                if (totalSize > MAX_IMAGES_SIZE) {
                    addAlert(
                        "warning",
                        "You can add at most " + MAX_IMAGES_SIZE / 1e6 + " MB"
                    );
                    return; // Return to prevent further execution
                }

                // Process each file
                Array.from(files).forEach((file) => {
                    if (file.type.startsWith("image/")) {
                        loadImage(file)
                            .then((imageSrc) => {
                                // Check for duplicate image URL
                                const isDuplicate = this.images.some(
                                    (image) => image === imageSrc
                                );
                                if (!isDuplicate) {
                                    this.images.push(imageSrc); // Store the image source in the array
                                } else {
                                    addAlert(
                                        "warning",
                                        "This image is already added."
                                    );
                                }
                            })
                            .catch((error) => {
                                addAlert(
                                    "error",
                                    "Error loading image: " + error
                                );
                            });
                    } else {
                        addAlert("warning", file.name + " is not an image.");
                    }
                });
            }
        },
    },
    mounted() {
        this.chatSetup();
        this.connectWebSocket();
        watch(
            authUserId,
            (newUserId) => {
                if (newUserId != this.currentUserId && isAuth) {
                    this.chatSetup();
                }
            },
            { immediate: true }
        );
    },
    beforeUnmount() {
        if (this.socket) {
            this.socket.close();
        }
    },
};
</script>
