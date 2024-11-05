<template>
    <div  v-if="activity.check_in_allowed">
        <h1 @allow-checked-in="fetchCheckInCode" class="card-title text-4xl mr-2 text-base-content align-center">Check-In code: </h1>
        <br>
        <h1 class="card-title text-8xl mr-2 align-center text-accent">{{ activity.check_in_code }}</h1>
        <br>
        <button 
            @click="closeCheckIn"
            type="button" 
            class="btn btn-error hover:brightness-50"
        >
            Close Check-in
        </button>
    </div>
    <div  v-else>
        <button
            @click="allowCheckIn"
            class="btn btn-accent ml-2 mr-2"
        >
            Get Check-In code
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue'
import { useRoute } from 'vue-router'
import apiClient from "@/api";
import { addAlert } from "@/functions/AlertManager";
import { createPutRequest } from "@/functions/HttpRequest.js";

const emit = defineEmits(["allow-checked-in", "closed-checked-in"]) 
const route = useRoute();

const activityId = ref(0);
const activity = ref({});
const isDarkTheme = ref(true);

async function fetchCheckInCode() {
    /**
    * Get data from specific activity including participant detail.
    */
    try {
    const response = await apiClient.get(
        `/activities/${activityId.value}`
    );
    activity.value = response.data;
    } catch (error) {
        console.error("Error fetching activity:", error);
        addAlert(
            "warning",
            "Activity already started or No such activity."
        );
    }
}

async function allowCheckIn() {
    /*
        * Attempt to join activity.
        */
    try {
        const response = await createPutRequest(
            `/activities/check-in/${activityId.value}/?status=open`,
            {}
        );
        addAlert("success", response.data.message);
        emit("allow-checked-in")
        fetchCheckInCode();
    } catch (error) {
        if (error.response && error.response.data) {
            addAlert("error", error.response.data.message); // Show error message from backend
        } else {
            console.error(error)
            addAlert(
                "error",
                "An unexpected error occurred. Please try again later."
            );
        }
    }
}

async function closeCheckIn() {
    /**
     * Make check-in unavailable.
     */
    try {
        const response = await createPutRequest(
            `/activities/check-in/${activityId.value}/?status=close`,
            {}
        );
        addAlert("success", response.data.message);
        emit("closed-checked-in")
        fetchCheckInCode(); //Fetch Activity
    } catch (error) {
        console.error("Error fetching activity:", error);
        addAlert(
            "warning",
            "Activity already started or No such activity."
        );
    }   
}

onMounted(() => {
    activityId.value = route.params.id;
    isDarkTheme.value = window.matchMedia(
        "(prefers-color-scheme: dark)"
    ).matches;
    window
        .matchMedia("(prefers-color-scheme: dark)")
        .addEventListener("change", (e) => {
            isDarkTheme.value = e.matches;
        });
    fetchCheckInCode();
})

</script>
