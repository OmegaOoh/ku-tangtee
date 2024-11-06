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
                    <h2 class="card-title flex justify-center overflow-visible">    
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
                                v-model='bio'
                                class='textarea textarea-primary w-full mb-4 resize-none'
                                placeholder='Share a little about yourself'
                                :maxlength='256'
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
                    <h2 class="card-title flex justify-center overflow-visible">    
                        <ul class="steps w-fit overflow-visible">
                            <li class="step step-primary"></li>
                            <li class="step step-primary">Education Info</li>
                        </ul>
                    </h2>
                    
                    <div class="form-control w-full">
                        <div class="label"> 
                            <span class='text-base-content text-lg'> KU Generation </span>
                            <span class='text-primary text-sm'> required </span>
                        </div>
                        <input
                            v-model='kuGen'
                            id="ku-gen-field"
                            type='number'
                            placeholder='e.g. 83'
                            class='input input-bordered input-primary w-full mb-4'
                            :max="getMaxKuGeneration()"
                            min=1
                        />
                    </div>

                    <div class="form-control w-full">
                        <div class="label"> 
                            <span class='text-base-content text-lg'> Faculty </span>
                            <span class='text-primary text-sm'> required </span>
                        </div>
                        <input
                            v-model='faculty'
                            type='text'
                            id="faculty-field"
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
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'
import { isAuth, login, email, fName, lName, userId } from "@/functions/Authentications";
import { addAlert } from "@/functions/AlertManager";
import { createPostRequest } from "@/functions/HttpRequest";
import apiClient from "@/api";

const KU_ESTABLISHED_YEAR = 1940

// Router
const router = useRouter();


// Variable
const nickname= ref('');
const pronoun= ref('');
const bio= ref('');
const kuGen= ref('');
const faculty= ref('');
const major= ref('');


const scrollCarousel = (index) => {
    /**
     * Function to scroll the carousel using index
     * This function return nothing
     */
    const carousel = document.getElementById('carousel');
    let carouselW = carousel.clientWidth;
    const targetPixel = (carouselW * index) + 1;
    carousel.scrollTo(targetPixel, 0);
}

/**
 *  Validator
 */

const kuGenError = (isError) => {
    /**
     * Set component of kuGen field to be error/ normal according to isErrorParameter
     * @param isError: bool
     * this function return nothing
     */
    const component = document.getElementById('ku-gen-field');
    if (isError) {
        component.classList.remove('textarea-primary');
        if (!component.classList.contains('textarea-error')) {
            component.classList.add('textarea-error');
        }
        
    }
    else {
        if (!component.classList.contains('textarea-primary')) {
            component.classList.add('textarea-primary');
        }
        component.classList.remove('textarea-error');
    }
}

const validateInput = () => {
    /**
     * Function to validate the input.
     * @return true if all input were valid.
     */
    var validInput = true;
    
    if (kuGen.value == null || kuGen.value == '') {
        kuGenError(true)
        validInput = false
    }
    else {
        kuGenError(false)
    }
    if (kuGen.value != ''){
        if (kuGen.value < 1) {
            kuGenError(true)
            addAlert('warning', "Your KU Generation must be at least 1");
            validInput = false;
        }
        else if (kuGen.value > getMaxKuGeneration()) {
            kuGenError(true)
            addAlert('warning', ('Your KU Generation must be less than or equal to ' + this.getMaxKuGeneration()))
            validInput = false;
        }
        else {
            kuGenError(false)
        }
    }
    const component = document.getElementById('faculty-field')
    if (faculty.value == '') {
        validInput = false;
        component.classList.remove('input-primary')
        if (!component.classList.contains('input-error')) {
            component.classList.add('input-error')
        }
    }
    else {
        component.classList.remove('input-error')
        if (!component.classList.contains('input-primary')) {
            component.classList.add('input-primary')
        }
    }
    return validInput
}

/**
 * Utils
 */

const getMaxKuGeneration = () => {
    /**
     * Get Maximum possible KU generation
     */
    const currentYear = (new Date()).getFullYear();
    return currentYear - KU_ESTABLISHED_YEAR;
}


const goNext = () => {
    /**
     * Redirect user to page in next params
     */
    const nextPath = router.currentRoute.value.query.next;
    if (nextPath == `/create-profile/` || nextPath == '' || !nextPath) {
        router.push('/')
    }
    else {
        router.push(nextPath)
    }
}

const submitProfile = async() => {
    /**
     * Function to submit data from form to the backend
     * This function return nothing
     */
    if (!validateInput()) {
        return
    }
    await createPostRequest(`/profile/`,
        {
            "user": userId,
            "nick_name": nickname.value,
            "pronoun": pronoun.value,
            "ku_generation": kuGen.value,
            "faculty": faculty.value,
            "major": major.value,
            "about_me": bio.value,
        }
    )
    goNext()
    addAlert('success', 'Your profile has been created successfully! Welcome to KU Tangtee!')
}

onMounted(async () => {
    const profileResponse = await apiClient.get(`profile/`)
    if (profileResponse.data.has_profile) {
        addAlert('info', "You already has the profile.")
        this.goNext()
    }
})

</script>