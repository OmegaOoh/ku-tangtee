<template>
    <div>
        <ul ref="messageList">
            <li v-for="(message, index) in messages" :key="index">
                {{ message.message }}
            </li>
        </ul>
        <input
            v-model="newMessage"
            placeholder="Start your chat"
            @keyup.enter="sendMessage"
        />
        <button class="btn-primary" @click="sendMessage">Send</button>
    </div>
</template>

<script>
import apiClient from "@/api";
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
        async fetchMessages() {
            this.messages = [];
            try {
                const response = await apiClient.get(
                    `/chat/${this.activityId}/`
                );
                this.messages = response.data;
            } catch (error) {
                console.error("Error fetching messages:", error);
            }
        },
        scrollToBottom() {
            const messageList = this.$refs.messageList;
            messageList.scrollTop = messageList.scrollHeight;
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
