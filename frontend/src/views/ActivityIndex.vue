<template>
  <div>
    <h1>Activities List</h1>
    <ul v-if="activities.length">
      <li v-for="activity in activities" :key="activity.id">
        <h2>
          {{ activity.name }}
        </h2>
        <p>{{ activity.detail }}</p>
        <p>Start date: {{ new Date(activity.date).toLocaleString() }}</p>
        <router-link :to="{ path: `/activities/${activity.id}` }">
            <button @click="viewActivity(activity.id)">View</button>
        </router-link>
      </li>
    </ul>
    <p v-else>No upcoming activities found.</p>
  </div>
</template>

<script>
import apiClient from '@/api'; // Get API

export default {
  data() {
    return {
      activities: [],
    };
  },
  mounted() {
    this.fetchActivities();
  },
  methods: {
    async fetchActivities() {
      try {
        const response = await apiClient.get('/activities/'); // Trying to get data from API
        this.activities = response.data;
      } catch (error) {
        console.error("Error fetching activities:", error);
        if (error.response) {
          console.error("Response data:", error.response.data);
          console.error("Response status:", error.response.status);
        }
      }
    },
    viewActivity(activityId) {
      // Navigate to the detail page of the activity without joining it
      this.$router.push(`/activities/${activityId}`); // Navigate to the activity detail page
    },
  },
};
</script>

