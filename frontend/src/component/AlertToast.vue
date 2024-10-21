<template>
    <div role="alert" class='fade' :class="alertClass" v-if="isVisible">
        <component :is="alertIcon" class="h-6 w-6 shrink-0 stroke-current"></component>
        <span>{{ content }}</span>
    </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'; 

// Define SVG Components
const InfoIcon = {
    template:
    `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
    </svg>`
};

const SuccessIcon = {
    template:
    `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>`
};

const WarningIcon = {
    template: 
    `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
    </svg>`
};

const ErrorIcon = {
    template:
    `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>`
};

const props = defineProps({
    content: {
        type: String,
        required: true,
    },
    type: {
        type: String,
        default: 'info',
    },
    isVisible: {
        type: Boolean,
        default: true,
    }
});

// Mapping alert types to classes and icons
const alertType = {
    success: 'alert alert-success',
    info: 'alert alert-info',
    warning: 'alert alert-warning',
    error: 'alert alert-error',
};

const alertTypeIcon = {
    success: SuccessIcon,
    info: InfoIcon,
    warning: WarningIcon,
    error: ErrorIcon,
};

// Computed properties for alert class and icon
const alertClass = computed(() => alertType[props.type] || alertType.info);
//const alertIcon = computed(() => alertTypeIcon[props.type] || alertTypeIcon.info);
const alertIcon = computed(() => {
    const icon = alertTypeIcon[props.type];
    console.log(icon); // Log the icon being used
    return icon || alertTypeIcon.info;
});

</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
    opacity: 0;
}
</style>