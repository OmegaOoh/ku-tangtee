<template>
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
        <button @click="fetchProfile" class="btn btn-secondary rounded-l-none">
            Search
        </button>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-1 gap-4 mb-2 ml-3">
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
                        {{ participant.first_name }} {{ participant.last_name }}
                    </p>
                    <div class="flex space-x-2">
                        <button
                            v-if="
                                !checkHost(participant.id) &&
                                !grantHost.includes(participant.id)
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
                                !removeHost.includes(participant.id)
                            "
                            class="btn btn-warning"
                            @click="handleDemote(participant.id)"
                        >
                            Demote
                        </button>
                        <button
                            v-if="
                                !checkHost(participant.id) &&
                                !grantHost.includes(participant.id)
                            "
                            class="btn btn-error"
                        >
                            Kick
                        </button>
                        <p
                            v-if="
                                removeHost.includes(participant.id) ||
                                grantHost.includes(participant.id)
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
</template>

<script>
import apiClient from "@/api";
import { createPutRequest } from "@/functions/HttpRequest.js";
import { addAlert } from "@/functions/AlertManager";
export default {
    data() {
        return {
            id: this.activityId,
            removeHost: [],
            grantHost: [],
            activity: {},
            people: [],
            hosts: [],
            name: "",
            searchKeyword: "",
        };
    },
    methods: {
        async fetchDetail() {
            /*
             * Get data from specific activity including participant detail.
             * This function does not return anything.
             */
            try {
                const response = await apiClient.get(
                    `/activities/${this.activityId}`
                );
                this.activity = response.data;
                this.name = this.activity.name;
                this.people = this.activity.participant;
                this.hosts = JSON.stringify(response.data.host);
                this.owner = this.activity.owner;
                console.log(this.people);
            } catch (error) {
                console.error("Error fetching activity:", error);
            }
        },
        async postUpdate() {
            /*
             * Attempt to update activity information.
             * This function does not return anything.
             */
            try {
                // Construct data to create POST request
                const data = {
                    remove_host: this.removeHost,
                    grant_host: this.grantHost,
                };
                const response = await createPutRequest(
                    `/activities/${this.activityId}/`,
                    data
                );
                this.removeHost = [];
                this.grantHost = [];
                addAlert("success", response.data.message);
                this.$emit("update-success");
                await this.fetchDetail();
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
        async fetchProfile() {
            /*
             * Attempt to update search participant.
             * This function does not return anything.
             */
            try {
                let response;
                response = await apiClient.get(
                    `/activities/${this.activityId}/search-participants/?keyword=${this.searchKeyword}`
                );
                this.people = response.data.map(
                    (participant) => participant.participant
                );
                console.log(this.people);
            } catch (error) {
                console.error("Error searching participant:", error);
            }
        },
        checkHost(userId) {
            /**
             * Check whether or not user is host of activity.
             * return None
             */
            return this.hosts.includes(userId);
        },
        checkOwner(userId) {
            /**
             * Check whether or not user is host of activity.
             * return None
             */
            return this.owner === userId;
        },
        handlePromote(userId) {
            this.grantHost.push(userId);
        },
        handleDemote(userId) {
            this.removeHost.push(userId);
        },
    },
    mounted() {
        this.activityId = this.$route.params.id;
        this.isDarkTheme = window.matchMedia(
            "(prefers-color-scheme: dark)"
        ).matches;
        window
            .matchMedia("(prefers-color-scheme: dark)")
            .addEventListener("change", (e) => {
                this.isDarkTheme = e.matches;
            });
        this.fetchDetail();
    },
};
</script>
