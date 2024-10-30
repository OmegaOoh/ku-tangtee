<template>
    <div :class='divClass'>
        <div :class='componentClass' v-for="(imageSrc, index) in images" :key="index">
            <img
                    v-if="imageSrc"
                    v-lazy="imageSrc"
                    :class='"object-contain size-full" + imageClass'
            />
            
        </div>
    </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
    images: {
        type: Array,
        Required: true,
    },
    removable: {
        type: Boolean,
        Required: false
    },
    componentClass: {
        type: String,
        Required: false,
        default: '',
    },
    divClass: {
        type: String,
        Required: false,
        default: 'w-fit grid grid-cols-5 gap-1',
    },
    imageClass: {
        type: String,
        Required: false,
        default: '',
    }
    
})
</script>