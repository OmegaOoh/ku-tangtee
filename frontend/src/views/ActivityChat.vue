<template>
    <div>
        <ul ref="messageList" class="overflow-y-auto h-[75vh]">
            <li v-for="(message, index) in messages" :key="index">
                <div class="chat chat-start">
                    <div class="chat-header">
                        {{ message.first_name }}
                        {{ message.last_name }}
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
                class="textarea textarea-primary w-full mb-2"
                :maxlength="1024"
                @keydown.exact.enter.prevent="sendMessage"
                @keydown.shift.enter.prevent="insertNewLine"
                rows="1"
            ></textarea>
            <button class="btn btn-primary ml-2 mb-2" @click="sendMessage">
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
        };
    },
    methods: {
        connectWebSocket() {
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
                if (data.message) {
                    this.messages.push(data.message);
                }
                this.fetchMessages();
            };
            this.socket.onclose = () => {
                console.log("WebSocket connection closed");
            };
            this.socket.onerror = (error) => {
                console.error("WebSocket error: ", error);
            };
        },
        sendMessage() {
            if (this.newMessage.trim() === "") {
                return;
            }
            if (this.socket.readyState === WebSocket.OPEN) {
                console.log(this.newMessage);
                this.socket.send(
                    JSON.stringify({
                        message: this.newMessage,
                    })
                );
                this.newMessage = "";
            } else {
                console.log("WebSocket is not open.");
            }
        },
        insertNewLine() {
            this.newMessage += "\n";
        },
        async fetchMessages() {
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
            this.$nextTick(() => {
                const messageList = this.$refs.messageList;
                messageList.scrollTop = messageList.scrollHeight;
            });
        },
        formatTimestamp(timestamp) {
            return format(new Date(timestamp), "PPpp");
        },
        formatMessage(message) {
            return message.replace(/\n/g, "<br>");
        },
    },
    mounted() {
        this.connectWebSocket();
        this.fetchMessages();
    },
    beforeUnmount() {
        if (this.socket) {
            this.socket.close();
        }
    },
};
</script>
