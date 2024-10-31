<template>
    <div id='img-carousel' class='carousel w-full max-h-[50vh] py-6 my-2'>
        <div :id="'slide'+index" class="carousel-item relative w-full justify-center" v-for="(imageSrc, index) in images" :key="index">
            <img
                    v-if="imageSrc"
                    v-lazy="imageSrc"
                    @click="openModal(imageSrc)"
            />
            <div class="indicator">
                <div v-if="removable" class="absolute indicator-item right-0"> 
                    <button class="btn btn-circle btn-error hover:brightness-50 transition-all ease-in-out" @click="$emit('onRemove', index)">
                        <svg
                            class="swap-on fill-current"
                            xmlns="http://www.w3.org/2000/svg"
                            width="32"
                            height="32"
                            viewBox="0 0 512 512">
                            <polygon
                            points="400 145.49 366.51 112 256 222.51 145.49 112 112 145.49 222.51 256 112 366.51 145.49 400 256 289.49 366.51 400 400 366.51 289.49 256 400 145.49" />
                        </svg>
                    </button>
                </div>
            </div>

            <div class="absolute left-5 right-5 top-1/2 flex -translate-y-1/2 transform justify-between">
                <a @click.prevent="scrollCarousel(index - 1)" class="btn btn-circle">❮</a>
                <a @click.prevent="scrollCarousel(index + 1)" class="btn btn-circle">❯</a>
            </div>
        </div>
    </div>
    <div class="flex w-full justify-center gap-2 py-2">
        <a @click.prevent="scrollCarousel(index-1)" v-for="index in images.length" :key="index" class="btn btn-xs">{{index}}</a>
    </div>

    <ImagePreview
            v-if="isModalOpen"
            :imageSrc="selectedImage"
            :isOpen=isModalOpen
            @close="closeModal"
    />

</template>

<script setup>
import { defineProps, ref } from 'vue';
import ImagePreview from './ImagePreview.vue';

const props = defineProps({
    images: {
        type: Array,
        Required: true,
    },
    removable: {
        type: Boolean,
        Required: false
    }
})

function scrollCarousel(index) {
    /**
     * Function to scroll the carousel using index
     * This function return nothing
     */
    const carousel = document.getElementById('img-carousel');

    let carouselW = carousel.clientWidth;
    let actualIndex = index < 0 ? props.images.length - 1 : index; 
    actualIndex = actualIndex >= props.images.length ? 0 : actualIndex;

    const targetPixel = (carouselW * actualIndex) + 1;
    carousel.scrollTo(targetPixel, 0);
}

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