<template>
    <div class="w-full overflow-x-hidden">
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
                        <button v-if="isOwner"  class="absolute cursor-pointer hover:text-primary transition-colors ease-in-out duration-100 left-3 top-2" @click="editMode = true"> 
                                ✎ 
                        </button>
                        <div>
                            <div class="avatar indicator">
                                <span class="indicator-item indicator-bottom indicator-center badge badge-accent font-semibold">
                                    KU &nbsp;
                                    <span v-if="!editMode">{{ kuGen }}</span>
                                    <input v-else 
                                        v-model="kuGen"
                                        type="number"
                                        class="w-6 no-arrows px-1 bg-inherit underline"
                                        min="1"
                                        :max="getMaxKuGeneration()"
                                    >
                                </span>
                            
                                <div class="w-24 rounded-md">
                                    <img v-lazy="pfp"/>
                                </div>
                            </div>
                        </div>
                        <div class='flex-row ml-3 w-full'>
                            <span class="text-2xl font-semibold text-wrap break-words"> {{ user.first_name }} {{ user.last_name }} </span>
                            <span class="text-xs font-light"> {{user.username}} </span> 
                            <div v-if="!editMode">
                                <p class=" text-primary break-words text-wrap"> {{ faculty }} </p>
                                <p class="text-sm font-light text-accent break-words text-wrap"> {{ major }} </p>
                            </div>
                            <div v-else class="flex flex-col">
                                <input 
                                    v-model="faculty" 
                                    type="text" 
                                    placeholder="Faculty"
                                    class="w-[80%] rounded-md text-primary bg-base-200 border-1 my-3 px-2 outline-primary focus:outline-double border-primary"/>
                                <input 
                                    v-model="major" 
                                    type="text" 
                                    placeholder="Major"
                                    class="w-[80%] rounded-md text-accent bg-base-200 border-1 mb-3 px-2 outline-accent focus:outline-double"/>
                            </div>
                            <div v-if="bio || editMode">
                                <p class="pt-2 mb-2 text-sm font-semibold">Bio</p>
                                <textarea v-if="!editMode" v-model='bio' class="text-xs w-full resize-none bg-inherit overflow-hidden break-normal" disabled rows="2"></textarea>
                                <textarea v-else 
                                    v-model='bio' 
                                    placeholder="Share a little about yourself" 
                                    class="text-xs w-full resize-none overflow-hidden break-normal bg-base-200 p-2 rounded-md outline-primary focus:outline-double" 
                                    rows="2"
                                ></textarea>
                            </div>
                            <div v-if="editMode">
                                <button class="btn btn-secondary rounded-md absolute top-2 right-2 w-fit h-fit py-1" @click="submitData" >
                                    Save
                                </button>
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
                        :key="activity.activity_id"
                        @click="$router.push(`/activities/${activity.activity_id}`)"
                    >
                        <div class="card-body">
                            <h2 class="card-title line-clamp-1">
                                {{ activity.name }}
                            </h2>
                            <p>
                                <strong>Date and Time: </strong>
                                {{ formatTimestamp(activity.activity_date) }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import apiClient from '@/api';
import { watch } from 'vue';
import { isAuth, userId } from '@/functions/Authentications';
import { format } from "date-fns";
import { addAlert } from '@/functions/AlertManager';
import { createPutRequest } from '@/functions/HttpRequest';

const KU_ESTABLISHED_YEAR = 1940

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
            editMode: false,
            isOwner: false,
        }
    },
    methods: {
        async fetchUserData() {
            /**
             * Function to fetch data of user from backend.
             * this function return nothing.
             */
            const response = await apiClient.get(`/profile/${this.$route.params.username}`);
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
            const response = await apiClient.get(`/activities/get-recently/${this.user.id}?byDate=True`);
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
                return format(new Date(timestamp), "MMM/dd/yyyy, hh:mm a");
            } else {
                return "No date provided";
            }
        },
        checkOwn() {
            console.log(userId.value, this.user.id)
            if (this.user.id == userId.value) {
                this.isOwner = true;
            } else {
                this.isOwner = false;
            }
        },
        validateInput() {
            /**
             * Function to validate the input.
             * @return true if all input were valid.
             */
            var validInput = true;
            
            if (this.kuGen == null || this.kuGen == '') {
                validInput = false
                addAlert('error', 'KU Generation is required');
            }
            if (this.kuGen != ''){
                if (this.kuGen < 1) {
                    addAlert('warning', "Your KU Generation must be at least 1");
                    validInput = false;
                }
                if (this.kuGen > this.getMaxKuGeneration()) {
                    addAlert('warning', ('Your KU Generation must be less than or equal to ' + this.getMaxKuGeneration()))
                    validInput = false;
                }
            }
            if (this.faculty == '') {
                validInput = false;
                addAlert('error', 'Faculty is required')
            }
            return validInput;
        },
        getMaxKuGeneration() {
            /**
             * Get current max Ku Generation
             * @returns maximum ku generation (current years - established year)
             */
            const currentYear = (new Date()).getFullYear();
            return currentYear - KU_ESTABLISHED_YEAR;
        },
        async submitData() {
            if (!this.validateInput()) {
                return;// Invalid input return early
            }
            await createPutRequest(`/profile/${this.user.username}/`,
                {
                    "nick_name": this.nickname,
                    "pronoun": this.pronoun,
                    "ku_generation": this.kuGen,
                    "faculty": this.faculty,
                    "major": this.major,
                    "about_me": this.bio,
                }
            )
            addAlert('success', 'Your Profile has been edited successfully!')
            this.editMode=false
        }
        
    },
    async mounted() {
        try{
            await this.fetchUserData();
            this.fetchRecentActivities();
        } catch (e) {
            this.$router.push('/')
            addAlert('error', 'The profile does not exists.')
        }

        this.checkOwn();
        watch(userId, () => {
                if (isAuth) {
                    this.checkOwn();
                }
                else {
                    this.isOwner = false;
                }
            }
        )
    },
    watch: {
        '$route.params.username': function(newUsername, oldUsername) {
            if (newUsername != oldUsername) {
                console.log('I was here');
                this.fetchUserData();
                this.fetchRecentActivities();
                this.checkOwn();
            }
        }
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

.no-arrows {
    -moz-appearance: textfield;
    appearance: textfield;
}

.no-arrows::-webkit-inner-spin-button,
.no-arrows::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
</style>
