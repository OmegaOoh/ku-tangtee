<template>
    <div class="breadcrumbs text-lm size-fit my-6 mx-10 w-full h-fit overflow-visible">
        <ul>
            <li><a @click="$router.push('/');">Home</a></li>
            <li>Profile</li>
        </ul>
    </div>
    <div
        class="card p-2 bg-base-300 border-2 border-primary shadow-md rounded-lg m-6"
    >
        <div class="card-body">
            <div class="card p-4 bg-base-100 shadow-md rounded-lg w-full">
                <div class='card-body flex flex-row justify-start w-full'>
                    <div>
                        <div class="avatar indicator">
                            <p class="indicator-item indicator-bottom indicator-center badge badge-accent font-semibold">
                                KU {{kuGen}}
                            </p>
                        
                            <div class="w-24 rounded-md">
                                <img v-lazy="pfp" />
                            </div>
                        </div>
                    </div>
                    <div class='flex-row ml-3 w-full'>
                        <span class="text-2xl font-semibold text-wrap break-words"> {{ user.first_name }} {{ user.last_name }} </span>
                        <span class="text-xs font-light"> {{user.username}} </span>
                        <div>
                            <p class=" text-primary break-words text-wrap"> {{ faculty }} </p>
                            <p class="text-sm font-light text-accent break-words text-wrap"> {{ major }} </p>
                        </div>
                        <div v-if="bio">
                            <p class="pt-2 text-sm font-semibold">Bio</p>
                            <textarea v-model='bio' class="text-xs w-full resize-none bg-inherit overflow-hidden break-normal" disabled rows="2"></textarea>
                        </div>
                    </div>
                </div>
            </div>
            <div class="divider">
                Joined Activity
            </div>
            <div class="flex flex-col">
                <div class="card bg-base-200 w-full hover:border-2 border-primary transition-all ease-in-out duration-75 mb-4 cursor-pointer"
                    v-for="activity in recentActivity"
                    :key="activity.id"
                    @click="$router.push('/activities/activity.id')"
                >
                    <div class="card-body">
                        <h2 class="card-title line-clamp-1">
                            {{ activity.name }}
                        </h2>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import apiClient from '@/api';
import { format } from "date-fns";

export default {
    data() {
        return {
            user: [],
            faculty: '',
            major: '',
            bio: '',
            kuGen: '',
            pfp: '',
            recentActivity: [],
        }
    },
    methods: {
        async fetchUserData() {
            /**
             * Function to fetch data of user from backend.
             * this function return nothing.
             */
            const response = await apiClient.get(`/profile/${this.$route.params.username}`);
            console.log(response.data)
            this.user = response.data.user;
            this.faculty = response.data.faculty;
            this.major = response.data.major;
            this.kuGen = response.data.ku_generation;
            this.bio = response.data.about_me;
            this.pfp = response.data.profile_picture_url;
        },
        async fetchRecentActivities() {
            /**
             * Fetch data of recently joined activity.
             * this function returns nothing.
             */
            const response = await apiClient.get(`/activities/get-recently/${this.user.id}`);
            this.recentActivity = response.data;
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
    },
    async mounted() {
        await this.fetchUserData();
        this.fetchRecentActivities();
    }
}
</script>

<style scoped>
.line-clamp-2 {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    word-wrap: break-word;
    overflow: hidden;
    text-overflow: ellipsis;
}

.line-clamp-1 {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 1;
    line-clamp: 1;
    word-wrap: break-word;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
