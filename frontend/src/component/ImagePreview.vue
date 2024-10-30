<template>
        <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center backdrop-blur-md bg-black bg-opacity-40 z-10" @keypress="checkKey" @click="closeModal">
        <div class="rounded-lg p-4 relative" @click.stop>
            <img :src="imageSrc" class="max-w-full max-h-[80vh]" />
        </div>
    </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
    imageSrc: {
        type: String,
        required: true,
    },
    isOpen: {
        type: Boolean,
        required: true,
    },
});

const emit = defineEmits(['close']);

const closeModal = () => {
    emit('close');
};

const checkKey = (event) => {
    if (event.key === 'Escape') {
        closeModal();
    }
};

</script>
