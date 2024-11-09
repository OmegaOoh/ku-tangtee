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
                    class="card-body overflow-y-auto h-[70vh] break-words"
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
                            <div class="chat-bubble chat-bubble-secondary">
                                <div class='multi-line'
                                    v-html="markdownFormatter(message.message)"
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
                                                (image) => BASE_URL + image
                                            )
                                        "
                                    />
                                </div>
                            </div>
                        </div>
                    </li>
                </ul>
                <div
                    class="absolute flex justify-center z-10 bottom-2 right-1 left-1"
                >
                    <button
                        id="bottom-button"
                        class="btn btn-accent size-fit text-xl transition-all duration-300 ease-in-out opacity-0"
                        @click="
                            () => {
                                isAtBottom = true;
                                scrollToBottom();
                            }
                        "
                    >
                        ⇩
                    </button>
                </div>
            </div>
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
                            ref="messageTextarea"
                            v-model="newMessage"
                            placeholder="Start your chat"
                            class="resize-y size-full bg-inherit focus:outline-none align-middle pt-1.5 px-2"
                            :maxlength="1024"
                            @input="adjustHeight"
                            @keydown.exact.enter.prevent="sendMessage"
                            @keydown.shift.enter.prevent="insertNewLine"
                        ></textarea>
                    </div>

                    <button class="btn btn-primary mx-2" @click="sendMessage">
                        Send
                    </button>
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
import apiClient from '@/api';
import { format } from 'date-fns';
import { watch, ref, onMounted, onBeforeUnmount, nextTick} from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
    login,
    isAuth,
    userId as authUserId,
} from '@/functions/Authentications';
import { addAlert } from '@/functions/AlertManager';
import { loadImage, markdownFormatter } from '@/functions/Utils';
import ImageGrid from '@/component/ImageGrid.vue';

const LINE_HEIGHT = 24;
const MAX_AREA_ROW = 6;

const router = useRouter();
const route = useRoute();

const MAX_CONSECUTIVE_SAME_MSG  = 5

const MAX_IMAGE_COUNT = 5;
const MAX_IMAGES_SIZE = 50e6; // 50 MB

const BASE_URL = (() => {
    let url = process.env.VUE_APP_BASE_URL;
    if (url.endsWith('/')) {
        url = url.slice(0, -1);
    }
    return url;
})();

// Variables
const socket = ref(null);
const newMessage = ref('');
const messages = ref([]);
const activityId = ref(route.params.id);
const people = ref([]);
const currentUserId = ref(null);
const isJoined = ref(false);
const isAtBottom = ref(true);
const images = ref([]);

// Element Variables
const messageList = ref(null);
const messageTextarea = ref(null)

let last_msg = {};
let streak = 0;

/**
 * Message Websocket
 */

const connectWebSocket = () => {
    /*
     * Connect to websocket to observe the change of index.
     * Return Nothing
     */
    let new_socket = new WebSocket(
        `${process.env.VUE_APP_BASE_URL.replace(/^http/, 'ws').replace(
            /^https/,
            'wss'
        )}ws/chat/${activityId.value}`
    );
    socket.value = new_socket;
    socket.value.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const user_id = data.user_id;
        if (data.message) {
            messages.value.push({
                message: data.message,
                timestamp: new Date(),
                user_id: user_id,
                images: data.images,
            });
            scrollToBottom();
            if (!people.value.some((element) => element.id === user_id)) {
                fetchSingleProfile(user_id);
            }
        }
    };
    socket.value.onerror = (error) => {
        console.error('WebSocket error: ', error);
    };
};

const sendMessage = () => {
    /*
     * Send message using text in text area.
     * Return Nothing
     */
    let trimMessage = newMessage.value.trim();
    trimMessage = trimMessage.replace(/^(<br\s*\/?>\s*)+/g, ''); // remove leading <br>
    trimMessage = trimMessage.replace(/(\s*<br\s*\/?>)+$/g, ''); // remove trailing <br>
    
    if (trimMessage === ''  && (images.value.length == 0)) {
        return;
    }
    if (trimMessage == '') {
        trimMessage = ' ';
    }

    let msg = JSON.stringify({
                message: trimMessage,
                user_id: authUserId.value,
                images: images.value,
            })

    if (msg != last_msg) {
        last_msg = msg;
        streak = 1;
    }
    else {
        streak++;
    }

    if (streak >= MAX_CONSECUTIVE_SAME_MSG) {
        socket.value.close()
        addAlert('warning', 'You are spamming, BAD USER!')
        return;
    }

    if (socket.value.readyState === WebSocket.OPEN) {
        socket.value.send(msg);
        images.value = [];
        newMessage.value = '';
        nextTick(() => {adjustHeight();})
        handleScrollToBottom(); // Scroll to bottom unconditionally
    } else {
        addAlert('error', 'Chat is not connected, please refresh.')
        console.log('WebSocket is not open.');
    }
};

const insertNewLine = () => {
    /*
     * Add one line to the message.
     * Return Nothing
     */
    if (!messageTextarea.value) return;
    const cursorPositionStart = messageTextarea.value.selectionStart
    const cursorPositionEnd = messageTextarea.value.selectionEnd
    newMessage.value = newMessage.value.slice(0, cursorPositionStart) 
                        + '\n' 
                        + newMessage.value.slice(cursorPositionEnd);
    messageTextarea.value.selectionStart = messageTextarea.value.selectionEnd = cursorPositionStart + 1;
    adjustHeight();
};

const handleFileChange = (event) => {
    /*
     * Push value into images.
     * @params {image} image that uploads from input.
     * Return nothing.
     */
    const files = event.target.files;
    if (files.length > 0) {
        // Check total image count
        if (files.length + images.value.length > MAX_IMAGE_COUNT) {
            addAlert(
                'warning',
                'You can add at most ' + MAX_IMAGE_COUNT + ' pictures'
            );
            return;
        }

        // Calculate total size of current and new images
        let totalSize = images.value.reduce((sum, file) => sum + file.size, 0);

        Array.from(files).forEach((file) => {
            totalSize += file.size;
        });

        // Check if total size exceeds limit
        if (totalSize > MAX_IMAGES_SIZE) {
            addAlert(
                'warning',
                'You can add at most ' + MAX_IMAGES_SIZE / 1e6 + ' MB'
            );
            return; // Return to prevent further execution
        }

        // Process each file
        Array.from(files).forEach((file) => {
            if (file.type.startsWith('image/')) {
                loadImage(file)
                    .then((imageSrc) => {
                        // Check for duplicate image URL
                        const isDuplicate = images.value.some(
                            (image) => image === imageSrc
                        );
                        if (!isDuplicate) {
                            images.value.push(imageSrc); // Store the image source in the array
                        } else {
                            addAlert('warning', 'This image is already added.');
                        }
                    })
                    .catch((error) => {
                        addAlert('error', 'Error loading image: ' + error);
                    });
            } else {
                addAlert('warning', file.name + ' is not an image.');
            }
        });
    }
};

const chatSetup = async () => {
    await fetchProfile();
    await checkJoined();
    if (isJoined.value) {
        if (socket.value) {
            socket.value.close();
            connectWebSocket();
        }
        await fetchCurrentUser();
        await fetchMessages();
    }
};

/*
 * Fetch Data
 */

const fetchCurrentUser = async () => {
    /*
     * Get current user that is on the current browser tab.
     * Return Nothing
     */
    currentUserId.value = authUserId.value;
};

const fetchProfile = async () => {
    /*
     * Get attendee profiles.
     * Return Nothing
     */
    people.value = [];
    const response = await apiClient.get(`/activities/${activityId.value}/`);
    const activity = response.data;
    people.value = activity.participant;
};

const fetchSingleProfile = async (userId) => {
    /*
     * Get single attendee profile.
     * Return Nothing
     */
    const uid = Number(userId);
    const participant = await apiClient.get(`/get-user/${uid}/`);
    people.value.push(participant.data);
};

const fetchMessages = async () => {
    /*
     * Get all previous messages.
     * Return Nothing
     */
    messages.value = [];
    try {
        const response = await apiClient.get(`/chat/${activityId.value}/`);
        messages.value = response.data;
        scrollToBottom();
    } catch (error) {
        console.error('Error fetching messages:', error);
    }
};

/**
 * Checker
 */

const checkJoined = () => {
    /*
     * Check if current user joined the activity
     * return boolean whether or not user is joined
     */
    isJoined.value = people.value.some(
        (element) => element['id'] == authUserId.value
    );
};

/**
 * Formatting
 */

const formatTimestamp = (timestamp) => {
    /*
     * Format the timestamp into (Oct 22, 2024, 9:00 AM).
     *
     * @params {string} not yet formatted timestamp
     * @returns {string} formatted timestamp
     */
    return format(new Date(timestamp), 'PPp');
};

const adjustHeight = () => {
    if (!messageTextarea.value) { console.log('messageArea not found'); return}
    const textarea = messageTextarea.value;
    if (textarea) {
        textarea.style.height = `auto`;
        const scrollHeight = textarea.scrollHeight;
        const maxHeight = LINE_HEIGHT * MAX_AREA_ROW;
        textarea.style.height = `${Math.min(scrollHeight, maxHeight)}px`;
    }
};

/**
 * Scrolling
 */

const scrollToBottom = () => {
    /*
     * Scroll the page to the bottom.
     * Return Nothing
     */
    nextTick(() => {
        if (isAtBottom.value) {
            handleScrollToBottom();
        } else {
            scrollButtonVisibility(true);
        }
    });
};

const handleScrollToBottom = () => {
    if (!messageList.value) {
        return; // messageList is uninitialized
    }
    messageList.value.scrollTo(0, messageList.value.scrollHeight);
    isAtBottom.value = true; // Ensure that isAtBottom be true
    scrollButtonVisibility(false);
};

const scrollButtonVisibility = (visibility) => {
    /*
     * Handle Opacity of scrollButton
     * this function return nothing
     */
    const button = document.getElementById('bottom-button');
    if (visibility) {
        button.classList.remove('opacity-0');
    } else if (!button.classList.contains('opacity-0')) {
        button.classList.add('opacity-0');
    }
};

const handleScroll = () => {
    /*
     * Handle Scrolling events in message list.
     * This function return nothing.
     */
    if (!messageList.value) {
        return; //messageList is null return early
    }
    const scrollTop = messageList.value.scrollTop;
    const clientHeight = messageList.value.clientHeight;
    const scrollHeight = messageList.value.scrollHeight;

    // Check if the user is at the bottom
    isAtBottom.value = scrollTop + clientHeight >= scrollHeight - 10;
};

/**
 * Data Getter
 */

const getProfilePicture = (userId) => {
    /*
     * Get profile picture from specific user id.
     *
     * @params {Number} sender user id
     * @returns {string} profile picture url
     */
    const participant = people.value.find(
        (person) => person.id === Number(userId)
    );
    return participant ? participant.profile_picture_url : null;
};

const getFullName = (userId) => {
    /*
     * Get user fullname from specific user id.
     *
     * @params {Number} sender user id
     * @returns {string} user firstname and lastname
     */
    const participant = people.value.find(
        (person) => person.id === Number(userId)
    );
    return participant
        ? `${participant.first_name} ${participant.last_name}`
        : 'Unknown User';
};

/**
 * Navigation
 */

const goHome = () => {
    /*
     * Navigate back to index page
     * @returns Nothing
     */
    router.push(`/`);
};
const goDetail = () => {
    /*
     * Navigate user back to activity page.
     * @returns Nothing
     */
    router.push(`/activities/${activityId.value}`);
};

/**
 * Lifecycle Hooks
 */

onMounted(() => {
    chatSetup();
    connectWebSocket();
    watch(
        authUserId,
        (newUserId) => {
            if (newUserId != currentUserId.value && isAuth) {
                chatSetup();
            }
        },
        { immediate: true }
    );
});

onBeforeUnmount(() => {
    if (socket.value) {
        socket.value.close();
    }
});
</script>

<style scoped>
.multi-line {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    word-wrap: break-word;
}
</style>