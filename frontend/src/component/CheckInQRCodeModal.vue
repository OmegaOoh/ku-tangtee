<template>
    <div v-if="isOpen" id='modal' 
        class="fixed inset-0 flex items-center justify-center backdrop-blur-md bg-black bg-opacity-40 z-10 transition-all ease-in-out duration-200" 
        @click="closeModal">
        <div class="rounded-lg p-4 relative" @click.stop>
            <qrcode-vue :value="fullUrl" level="H" size="300"/>
        </div>
    </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue';
import QrcodeVue from 'qrcode.vue';

const props = defineProps({
    code: {
        type: String,
        required: true,
    },
    isOpen: {
        type: Boolean,
        required: true,
    },
});

const fullUrl = ref(`${window.location.href}?code=${props.code}`);

const emit = defineEmits(['close']);

const closeModal = () => {
    const modal = document.getElementById('modal')
    modal.classList.add('opacity-0')
    setTimeout(() => { emit('close') }, 200)
};

</script>
