<template>
    <div v-if="!isAuth" class="flex justify-center">
        <div class="card w-[80%] h-fit m-6 bg-base-300 border-2 border-warning">
            <div class="card-body">
                <h2 class="card-title">Please Login</h2>
                <p>Profile Creation need for user to be authenticated</p>
                <div class="card-actions justify-end">
                    <button class="btn btn-warning " @click="login">login</button>
                </div>
            </div>
        </div>
    </div>

    <div v-else id='carousel' class="carousel mx-5">
        <div class="carousel-item w-full">
            <div class="card w-full h-fit p-6 bg-base-300 border-2 border-primary shadow-md rounded-lg m-6">
                <div class="card-body">
                    <h2 class="card-title flex justify-center">    
                        <ul class="steps w-[30%] stroke-base-content">
                            <li class="step step-primary">User Information</li>
                            <li class="step step-neutral"></li>
                        </ul>
                    </h2>
                    <div class='flex flex-row w-full gap-6'>
                        <div class="form-control w-full">
                            <div class="label"> 
                                <span class='text-base-content text-lg'> Email </span>
                            </div>
                            <input
                                type='text'
                                :placeholder="email"
                                class='input input-bordered input-primary w-full mb-4'
                                disabled
                            />
                        </div>

                        <div class="form-control w-full">
                            <div class="label"> 
                                <span class='text-base-content text-lg'> Full Name </span>
                            </div>
                            <input
                                type='text'
                                :placeholder="fName + ' ' + lName"
                                class='input input-bordered input-primary w-full mb-4'
                                disabled
                            />
                        </div>
                    </div>
                    
                    <div class="form-control w-full">
                        <div class="label"> 
                            <span class='text-base-content text-lg'> Nickname </span>
                        </div>
                        <input
                            v-model='nickname'
                            id='nick-field'
                            type='text'
                            placeholder='Nickname'
                            class='input input-bordered input-primary w-full mb-4'
                            :maxlength='30'
                            required
                        />
                    </div>
                    <div class="form-control w-full">
                        <div class="label"> 
                            <span class='text-base-content text-lg'> Pronoun </span>
                        </div>
                        <input
                            v-model='pronoun'
                            id='pronoun-field'
                            type='text'
                            placeholder='Pronoun'
                            class='input input-bordered input-primary w-full mb-4'
                            :maxlength='20'
                        />
                    </div>

                    <div class="form-control w-full">
                            <div class="label">
                                <span class='text-base-content'> Bio </span>
                            </div>
                            <textarea
                                v-model='activityDetail'
                                id='bio-field'
                                class='textarea textarea-primary w-full mb-4 resize-none'
                                placeholder='Bio'
                                :maxlength='1024'
                                rows="4"
                            >
                            </textarea>
                    </div>
                    <div class="card-actions justify-end">
                        <button class="btn btn-primary" @click="scrollCarousel(1)">Next</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="carousel-item w-full">
            <div class="card w-full h-fit p-6 bg-base-300 border-2 border-primary shadow-md rounded-lg m-6">
                <div class="card-body">
                    <h2 class="card-title flex justify-center">    
                        <ul class="steps w-[30%]">
                            <li class="step step-primary"></li>
                            <li class="step step-primary">Education Info</li>
                        </ul>
                    </h2>
                    
                    <div class="form-control w-full">
                        <div class="label"> 
                            <span class='text-base-content text-lg'> KU Generation </span>
                        </div>
                        <input
                            v-model='kuGen'
                            type='numeric'
                            placeholder='e.g. 83'
                            class='input input-bordered input-primary w-full mb-4'
                            :max="(Date().getFullYear) - 1940"
                        />
                    </div>

                    <div class="form-control w-full">
                        <div class="label"> 
                            <span class='text-base-content text-lg'> Faculty </span>
                        </div>
                        <input
                            v-model='faculty'
                            type='text'
                            placeholder='e.g. Engineering, Science'
                            class='input input-bordered input-primary w-full mb-4'
                            :maxlength='100'
                        />
                    </div>

                    <div class="form-control w-full">
                        <div class="label"> 
                            <span class='text-base-content text-lg'> Major </span>
                        </div>
                        <input
                            v-model='major'
                            type='text'
                            placeholder='e.g. Software and Knowledge Engineering, Computer Engineering'
                            class='input input-bordered input-primary w-full mb-4'
                            :maxlength='100'
                        />
                    </div>
                    
                    <div class="card-actions justify-between">
                        <button class="btn btn-accent" @click="scrollCarousel(0)">Back</button>
                        <button class="btn btn-primary" @click="submitProfile">Submit</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
import {isAuth, login, email, fName, lName } from "@/functions/Authentications";
</script>

<script>
export default {
    methods: {
        scrollCarousel(index) {
            /**
             * Function to scroll the carousel using index
             * This function return nothing
             */
            const carousel = document.getElementById('carousel');
            let carouselW = carousel.clientWidth;
            const targetPixel = (carouselW * index) + 1;
            carousel.scrollTo(targetPixel, 0);
        },
        submitProfile() {
            /**
             * Function to submit data from form to the backend
             * This function return nothing
             */
            console.log('To be implement :-)')
        }
    },
}
</script>