<template>
    <div class="flex items-center gap-2">
        <div
            v-for="(imageSrc, index) in images"
            :key="index"
            class="relative rounded-md overflow-hidden"
            :class="componentSize"
        >
            <img
                v-if="imageSrc"
                :src="imageSrc"
                class="object-cover w-full h-full"
                @click="openModal(imageSrc)"
            />
            <button
                v-if="removable"
                class="hover:opacity-50 absolute top-2 right-2"
                @click="$emit('onRemove', index)"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                >
                    <line x1="18" y1="6" x2="6" y2 ="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
            </button>
        </div>
        <ImagePreview
            v-if="isModalOpen"
            :imageSrc="selectedImage"
            :isOpen="isModalOpen"
            @close="closeModal"
        />
    </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue';
import ImagePreview from './ImagePreview.vue';

defineProps({
    images: {
        type: Array,
        required: true,
    },
    removable: {
        type: Boolean,
        required: false,
    },
    componentSize: {
        type: String,
        required: true,
    }
});

defineEmits('onRemove');

const isModalOpen = ref(false);
const selectedImage = ref('');

const openModal = (imageSrc) => {
    selectedImage.value = imageSrc;
    isModalOpen.value = true;
};

const closeModal = () => {
    isModalOpen.value = false;
    selectedImage.value = '';
};

</script>