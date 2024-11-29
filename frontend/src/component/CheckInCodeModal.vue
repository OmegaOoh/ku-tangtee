<template>
    <div
        v-if="isOpen"
        id="code-modal"
        class="fixed inset-0 flex items-center justify-center backdrop-blur-md bg-black bg-opacity-40 z-10 transition-all ease-in-out duration-200"
        @click="closeModal"
    >
        <div
            class="card bg-base-300 border-2 border-primary rounded-lg p-4 relative"
            @click.stop
        >
            <div>
                <h1
                    class="card-title text-4xl mr-2 text-base-content align-center"
                >
                    Check-In code:
                </h1>
                <br />
                <h1 class="card-title text-8xl mr-2 align-center text-accent">
                    {{ code }}
                </h1>
                <br />
                <button
                    @click="closeCheckIn"
                    type="button"
                    class="btn btn-error hover:brightness-50"
                >
                    Close Check-in
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
import { ref, onMounted, defineProps, defineEmits } from 'vue';
import apiClient from '@/api';
import { addAlert } from '@/functions/AlertManager';
import { createPutRequest } from '@/functions/HttpRequest.js';

const emit = defineEmits(['allow-checked-in', 'closed-checked-in']);

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

const code = ref('XXXXXX');
const check_in_allowed = ref(true);

async function fetchCheckInCode() {
    /**
     * Get data from specific activity including participant detail.
     */
    try {
        const response = await apiClient.get(`activities/check-in/${props.id}/`);
        code.value = response.data.check_in_code;
        check_in_allowed.value = response.data.check_in_allowed;
    } catch (error) {
        addAlert(
            'error',
            error.response?.data?.message ||
                'An unexpected error occurred. Please try again later.'
        );
    }
}

async function closeCheckIn() {
    /**
     * Make check-in unavailable.
     */
    const response = await createPutRequest(
        `/activities/check-in/${props.id}/?status=close`,
        {}
    );
    if (!response) return; // Not Success
    addAlert('warning', 'Check in closed');
    check_in_allowed.value = false;
    closeModal();
}

const closeModal = () => {
    const modal = document.getElementById('code-modal');
    modal.classList.add('opacity-0');
    setTimeout(() => {
        emit('close', check_in_allowed.value);
    }, 200);
};

onMounted(() => {
    fetchCheckInCode();
});
</script>
