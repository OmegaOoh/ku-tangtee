<template>
    <div>
        <h1>{{ activity.name }}</h1>
        <p><strong>Details:</strong> {{ activity.detail }}</p>
        <p><strong>Date:</strong> {{ new Date(activity.date).toLocaleString() }}</p>
        <p><strong>Max People:</strong> {{ activity.max_people }}</p>
        <p><strong>Joined People:</strong> {{ activity.people }}</p>

        <button v-if="canJoin" @click="joinActivity">Join Activity</button>
        <p v-else>This activity cannot be joined.</p>

        <router-link to="/">Back to Activities</router-link>
    </div>
</template>

<script>
import apiClient from '@/api';
export default {
    data() {
        return {
            activity: {},
            canJoin: true,
        };
    },
    methods: {
        async fetchActivity() {
            try {
                const response = await apiClient.get(`/activities/${this.activityId}`);
                this.activity = response.data;
                this.canJoin = this.activity.can_join; // Adjust this based on your backend logic
            } catch (error) {
                console.error('Error fetching activity:', error);
            }
        },
        async joinActivity() {
            try {
                const response = await apiClient.post(`/activities/${this.activityId}/join`);
                alert(response.data.message);
            } catch (error) {
                if (error.response && error.response.data) {
                    alert(error.response.data.error); // Show error message from backend
                } else {
                    alert("An unexpected error occurred. Please try again later.");
                }
            }
        }
    },
    mounted() {
        this.activityId = this.$route.params.id; 
        this.fetchActivity();
    },
};
</script>
