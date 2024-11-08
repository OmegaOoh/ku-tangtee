<template>
    <div
        v-if="isOpen"
        id="edit-perm"
        class="fixed inset-0 flex items-center justify-center backdrop-blur-md bg-black bg-opacity-40 z-10 transition-all ease-in-out duration-200"
        @click="closeModal"
    >
        <div
            class="rounded-lg p-4 relative card bg-base-300 border-2 border-primary w-[75%] h-[80vh] overflow-y-auto"
            @click.stop
        >
            <h2 class="card-title text-2xl mr-2 text-base-content mb-2">
                Manage Participant Permissions
            </h2>
            <div class="flex my-5 w-full">
                <input
                    v-model="searchKeyword"
                    @keydown.enter="fetchProfile"
                    class="input input-bordered w-full gap-2 rounded-r-none"
                    placeholder="Search"
                />
                <button
                    @click="fetchProfile"
                    class="btn btn-secondary rounded-l-none"
                >
                    Search
                </button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-1 gap-4 mb-2 ml-3">
                <div v-if="people.length === 0">
                    <p class="text-error text-lg">No participant match</p>
                </div>

                <div
                    v-for="participant in people"
                    :key="participant.id"
                    class="card bg-base-100 shadow-lg p-4 rounded-lg border-primary hover:border-2 cursor-pointer transition-all duration-75 ease-in-out"
                >
                    <div class="flex items-center space-x-4">
                        <!-- Profile Picture Container -->
                        <div class="indicator w-12 h-12 flex-shrink-0">
                            <img
                                v-lazy="participant.profile_picture_url"
                                alt="Profile Picture"
                                class="w-full h-full rounded-full object-cover"
                                @error="handleImageError"
                            />
                            <p
                                v-if="hosts.includes(participant.id)"
                                class="indicator-item indicator-bottom indicator-center badge badge-secondary"
                            >
                                Host
                            </p>
                        </div>

                        <!-- Name and Action Buttons -->
                        <div class="flex-1 min-w-0">
                            <p class="font-medium truncate">
                                {{ participant.first_name }}
                                {{ participant.last_name }}
                            </p>
                            <div class="flex space-x-2">
                                <button
                                    v-if="
                                        !checkHost(participant.id) &&
                                        !grantHost.includes(participant.id) &&
                                        !kickedParticipant.includes(
                                            participant.id
                                        )
                                    "
                                    class="btn btn-primary"
                                    @click="handlePromote(participant.id)"
                                >
                                    Promote
                                </button>
                                <button
                                    v-if="
                                        checkHost(participant.id) &&
                                        !checkOwner(participant.id) &&
                                        !removeHost.includes(participant.id) &&
                                        !kickedParticipant.includes(
                                            participant.id
                                        )
                                    "
                                    class="btn btn-warning"
                                    @click="handleDemote(participant.id)"
                                >
                                    Demote
                                </button>
                                <button
                                    v-if="
                                        !checkHost(participant.id) &&
                                        !grantHost.includes(participant.id) &&
                                        !kickedParticipant.includes(
                                            participant.id
                                        )
                                    "
                                    class="btn btn-error"
                                    @click="handleKick(participant.id)"
                                >
                                    Kick
                                </button>
                                <p
                                    v-if="
                                        removeHost.includes(participant.id) ||
                                        grantHost.includes(participant.id) ||
                                        kickedParticipant.includes(
                                            participant.id
                                        )
                                    "
                                    class="text-warning"
                                >
                                    Pending Update
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex justify-end">
                <button class="btn btn-accent" @click="postUpdate">
                    Update Permission
                </button>
            </div>
            <button
                class="absolute btn btn-circle btn-ghost top-1 right-1"
                @click="closeModal"
            >
                <svg
                    class="swap-on fill-current"
                    xmlns="http://www.w3.org/2000/svg"
                    width="32"
                    height="32"
                    viewBox="0 0 512 512"
                >
                    <polygon
                        points="400 145.49 366.51 112 256 222.51 145.49 112 112 145.49 222.51 256 112 366.51 145.49 400 256 289.49 366.51 400 400 366.51 289.49 256 400 145.49"
                    />
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup>
import apiClient from "@/api";
import { ref, defineProps, defineEmits, onMounted } from "vue";
import { createPutRequest } from "@/functions/HttpRequest.js";
import { addAlert } from "@/functions/AlertManager";

const emit = defineEmits(["update-success", "close"]);
const removeHost = ref([]);
const grantHost = ref([]);
const kickedParticipant = ref([]);
const activity = ref({});
const people = ref([]);
const hosts = ref([]);
const name = ref("");
const searchKeyword = ref("");
const detail = ref("");
const owner = ref(0);
const isDarkTheme = ref(false);

const props = defineProps({
    id: {
        type: String,
        required: true,
    },
    isOpen: {
        type: Boolean,
        required: true,
    },
});

const fetchDetail = async () => {
    /**
     * Get data from specific activity including participant detail.
     * This function does not return anything.
     */
    try {
        const response = await apiClient.get(`/activities/${props.id}`);
        activity.value = response.data;
        hosts.value = response.data.host;
        name.value = activity.value.name;
        people.value = activity.value.participant;
        owner.value = response.data.owner;
        detail.value = activity.value.detail;
    } catch (error) {
        console.error("Error fetching activity:", error);
    }
};
const postUpdate = async () => {
    /*
     * Attempt to update activity information.
     * This function does not return anything.
     */
    try {
        // Construct data to create POST request
        const data = {
            remove_host: removeHost.value,
            grant_host: grantHost.value,
            attendee_to_remove: kickedParticipant.value,
            owner: owner.value,
            detail: detail.value,
            name: name.value,
        };
        const response = await createPutRequest(
            `/activities/${props.id}/`,
            data
        );
        removeHost.value = [];
        grantHost.value = [];
        kickedParticipant.value = [];
        addAlert("success", response.data.message);
        emit("update-success");
        await fetchDetail();
    } catch (error) {
        console.error(error);
        if (error.response && error.response.data) {
            addAlert("error", error.response.data.message); // Show error message from backend
        } else {
            addAlert(
                "error",
                "An unexpected error occurred. Please try again later."
            );
        }
    }
};
const fetchProfile = async () => {
    /*
     * Attempt to update search participant.
     * This function does not return anything.
     */
    try {
        let response;
        response = await apiClient.get(
            `/activities/${props.id}/search-participants/?keyword=${searchKeyword.value}`
        );
        people.value = response.data.map(
            (participant) => participant.participant
        );
        console.log(people.value);
    } catch (error) {
        console.error("Error searching participant:", error);
    }
};

const checkHost = (userId) => {
    /**
     * Check whether or not user is host of activity.
     * @return boolean value
     */
    return hosts.value.includes(userId);
};
const checkOwner = (userId) => {
    /**
     * Check whether or not user is owner of activity.
     * @return boolean value
     */
    return owner.value === userId;
};
const handlePromote = (userId) => {
    /**
     * Update grant host list.
     * return None
     */
    grantHost.value.push(userId);
};
const handleDemote = (userId) => {
    /**
     * Update remove host list.
     * return None
     */
    removeHost.value.push(userId);
};
const handleKick = (userId) => {
    /**
     * Update remove host list.
     * return None
     */
    kickedParticipant.value.push(userId);
};
const closeModal = () => {
    /**
     * Close the modal.
     * return None
     */
    const modal = document.getElementById("edit-perm");
    modal.classList.add("opacity-0");
    setTimeout(() => {
        emit("close");
    }, 200);
};
onMounted(() => {
    isDarkTheme.value = window.matchMedia(
        "(prefers-color-scheme: dark)"
    ).matches;
    window
        .matchMedia("(prefers-color-scheme: dark)")
        .addEventListener("change", (e) => {
            isDarkTheme.value = e.matches;
        });
    fetchDetail();
});
</script>
