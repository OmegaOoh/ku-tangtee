<template>
    <div
        v-if="isOpen"
        id="modal"
        class="fixed inset-0 flex items-center justify-center backdrop-blur-md bg-black bg-opacity-40 z-10 transition-all ease-in-out duration-200"
        @click="closeModal"
    >
        <div class="rounded-lg p-4 relative" @click.stop>
            <qrcode-vue
                :value="computedUrl"
                level="H"
                :size="300"
                render-as="svg"
            />
        </div>
    </div>
</template>

<script setup>
import { defineProps, defineEmits, onMounted, ref, watch, computed } from 'vue';
import apiClient from '@/api';
import { addAlert } from '@/functions/AlertManager';
import QrcodeVue from 'qrcode.vue';

const CHECK_IN_LOCATION = window.location.href;

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

// Make fullUrl reactive
const fullUrl = ref('');

const emit = defineEmits(['close']);

const updateUrl = async () => {
    let code = await fetchCheckInCode();
    fullUrl.value = CHECK_IN_LOCATION + '?code=' + code; // Update the reactive reference
};

const fetchCheckInCode = async () => {
    try {
        const response = await apiClient.get(`/activities/${props.id}`);
        return response.data.check_in_code;
    } catch (error) {
        console.error('Error fetching activity:', error);
        addAlert('warning', 'Activity already started or No such activity.');
    }
};

watch(
    () => props.isOpen,
    (newStatus) => {
        if (newStatus) {
            updateUrl();
        }
    }
);

onMounted(() => {
    updateUrl();
});

const computedUrl = computed(() => fullUrl.value);

const closeModal = () => {
    const modal = document.getElementById('modal');
    modal.classList.add('opacity-0');
    setTimeout(() => {
        emit('close');
    }, 200);
};
</script>
