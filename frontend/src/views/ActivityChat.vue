<template>
    <div>
        <ul ref="messageList" class="overflow-y-auto h-[80vh]">
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
                    <div
                        class="chat-bubble chat-bubble-primary"
                        v-html="formatMessage(message.message)"
                    ></div>
                </div>
            </li>
        </ul>
        <div class="flex justify-between items-center mt-2">
            <textarea
                v-model="newMessage"
                placeholder="Start your chat"
                class="textarea textarea-primary w-full mb-2 mx-2"
                :maxlength="1024"
                @keydown.exact.enter.prevent="sendMessage"
                @keydown.shift.enter.prevent="insertNewLine"
                rows="1"
            ></textarea>
            <button class="btn btn-primary mx-2 mb-2" @click="sendMessage">
                Send
            </button>
        </div>
    </div>
</template>

<script>
import apiClient from "@/api";
import { format } from "date-fns";
export default {
    data() {
        return {
            socket: null,
            newMessage: "",
            messages: [],
            activityId: this.$route.params.id,
            people: [],
            currentUserId: null,
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
                this.fetchProfile();
                const data = JSON.parse(event.data);
                if (data.message) {
                    this.messages.push({
                        message: data.message,
                        timestamp: new Date(),
                        user_id: data.user_id,
                    });
                    this.scrollToBottom();
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
            if (this.newMessage.trim() === "") {
                return;
            }
            if (this.socket.readyState === WebSocket.OPEN) {
                this.socket.send(
                    JSON.stringify({
                        message: this.newMessage,
                        user_id: this.currentUserId,
                    })
                );
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
            try {
                const response = await apiClient.get("/profile-pic/");
                this.currentUserId = response.data.user_id;
                console.log(this.currentUserId);
            } catch (error) {
                console.error("Error fetching current user:", error);
            }
        },
        async fetchProfile() {
            /*
             * Get attendee profiles.
             * Return Nothing
             */
            this.people = [];
            const participant = await apiClient.get(
                `/activities/get-participant/${this.activityId}/`
            );
            this.people = participant.data;
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
                messageList.scrollTop = messageList.scrollHeight;
            });
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
            return participant
                ? participant.profile_picture_url
                : "https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg";
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
    },
    async mounted() {
        await this.fetchCurrentUser();
        await this.fetchProfile();
        await this.fetchMessages();
        this.connectWebSocket();
    },
    beforeUnmount() {
        if (this.socket) {
            this.socket.close();
        }
    },
};
</script>
