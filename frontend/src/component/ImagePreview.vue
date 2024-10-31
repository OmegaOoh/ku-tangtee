<template>
        <div v-if="isOpen" id='modal' 
            class="fixed inset-0 flex items-center justify-center backdrop-blur-md bg-black bg-opacity-40 z-10 transition-all ease-in-out duration-200" 
            @click="closeModal">
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
    const modal = document.getElementById('modal')
    modal.classList.add('opacity-0')
    setTimeout(() => { emit('close') }, 200)
};

</script>
