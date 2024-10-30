<template>
    <div id='img-carousel' class='carousel w-full max-h-[50vh]' tabindex="-1" >
                        <div :id="'slide'+index" class="carousel-item relative w-full justify-center" v-for="(imageSrc, index) in images" :key="index">
                            <img
                                v-if="imageSrc"
                                v-lazy="imageSrc"
                            >
                            <div class="absolute left-5 right-5 top-1/2 flex -translate-y-1/2 transform justify-between">
                                <a @click.prevent="scrollCarousel(index - 1)" class="btn btn-circle">❮</a>
                                <a @click.prevent="scrollCarousel(index + 1)" class="btn btn-circle">❯</a>
                            </div>
                        </div>
                    </div>
                    <div class="flex w-full justify-center gap-2 py-2">
                        <a @click.prevent="scrollCarousel(index-1)" v-for="index in images.length" :key="index" class="btn btn-xs">{{index}}</a>

    </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
    images: {
        type: FileList,
        Required: true,
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
</script>