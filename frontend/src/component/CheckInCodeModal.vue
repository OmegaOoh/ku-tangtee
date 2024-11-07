<template>
<div v-if="isOpen" id='code-modal' 
    class="fixed inset-0 flex items-center justify-center backdrop-blur-md bg-black bg-opacity-40 z-10 transition-all ease-in-out duration-200" 
    @click="closeModal">
    <div class="card bg-base-300 border-2 border-primary rounded-lg p-4 h-2/5 w- relative" @click.stop>
        <div>
            <h1 class="card-title text-4xl mr-2 text-base-content align-center">Check-In code: </h1>
            <br>
            <h1 class="card-title text-8xl mr-2 align-center text-accent">{{ code }}</h1>
            <br>
            <button 
                @click="closeCheckIn"
                type="button" 
                class="btn btn-error hover:brightness-50"
            >
                Close Check-in
            </button>
        </div>
    </div>
</div>
</template>

<script setup>
import { ref, onMounted, defineProps,defineEmits } from 'vue'
import apiClient from "@/api";
import { addAlert } from "@/functions/AlertManager";
import { createPutRequest } from "@/functions/HttpRequest.js";

const emit = defineEmits(["allow-checked-in", "closed-checked-in"]) 

const props = defineProps({
    id: {
        type: String,
        required: true,
    },
    isOpen: {
        type: Boolean,
        required: true,
    }
})

const code = ref("XXXXXX"); 
const check_in_allowed = ref(true);

async function fetchCheckInCode() {
    /**
    * Get data from specific activity including participant detail.
    */
    try {
    const response = await apiClient.get(
        `/activities/${props.id}`
    );
    code.value = response.data.check_in_code;
    check_in_allowed.value = response.data.check_in_allowed;
    } catch (error) {
        console.error("Error fetching activity:", error);
        addAlert(
            "warning",
            "Activity already started or No such activity."
        );
    }
}

async function closeCheckIn() {
    /**
     * Make check-in unavailable.
     */
    try {
        await createPutRequest(
            `/activities/check-in/${props.id}/?status=close`,
            {}
        );
        addAlert("warning", "Check in closed");
        check_in_allowed.value = false;
        closeModal();
    } catch (error) {
        console.error("Error fetching activity:", error);
        addAlert(
            "warning",
            "Activity already started or No such activity."
        );
    }   
}

const closeModal = () => {
    const modal = document.getElementById('code-modal')
    modal.classList.add('opacity-0')
    setTimeout(() => { emit('close', check_in_allowed.value ) }, 200)
};

onMounted(() => {
    fetchCheckInCode();
})

</script>
