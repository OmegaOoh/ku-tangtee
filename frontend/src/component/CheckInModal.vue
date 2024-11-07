<template>
    <div v-if="isOpen" id='check-in-modal' 
        class="fixed inset-0 flex items-center justify-center backdrop-blur-md bg-black bg-opacity-40 z-10 transition-all ease-in-out duration-200" 
        @click="closeModal">
    <div class="rounded-lg p-4 relative card bg-base-300 border-2 border-primary h-fit w-2/3" @click.stop>
        <div class="card-body">
            <div class="form-control w-full">
                <h1 class="card-title text-base-content text-4xl font-semibold">Check-In Code: </h1>
                <div class="label"> 
                    <span id="code-field" class="text-error text-lg" hidden>
                        Check-in code must have 6 characters
                    </span>
                    <span id="invalid-code" class="text-error text-lg" hidden>
                        Invalid Check-In code
                    </span>
                </div>
                <input
                    v-model="checkInCode"
                    id="check-in-code-fields"
                    type="text"
                    class="input input-bordered input-primary w-full mb-4 text-8xl h-fit text-accent"
                    :maxlength="6"
                    required
                />
            </div>
            <br>
            <div class="flex justify-end">
                <button class="btn btn-accent" @click="postCheckIn">
                    Check-In
                </button>
            </div>
        </div>
        <button
            class="absolute btn btn-circle btn-ghost top-1 right-1"
            @click="closeModal"
        >
            <svg
                class="swap-on fill-current"
                xmlns="http://www.w3.org/2000/svg"
                width="32"
                height="32"
                viewBox="0 0 512 512"
            >
                <polygon
                    points="400 145.49 366.51 112 256 222.51 145.49 112 112 145.49 222.51 256 112 366.51 145.49 400 256 289.49 366.51 400 400 366.51 289.49 256 400 145.49"
                />
            </svg>
        </button>
    </div>
</div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';
import { addAlert } from "@/functions/AlertManager";
import { createPostRequest } from "@/functions/HttpRequest.js";

const props = defineProps({
    id: {
        type: String,
        required: true,
    },
    isOpen: {
        type: Boolean,
        required: true,
    }
})

const emit = defineEmits(['close', 'check-in-success']);

const checkInCode = ref("");

const postCheckIn = async () => {
    if (validateCheckInCode()){
        try {
            const response = await createPostRequest(
                `/activities/check-in/${props.id}/`,
                {
                    'check_in_code': checkInCode.value
                }
            );
            addAlert("success", response.data.message);
            emit("check-in-success");
        } catch (error) {
            if (error.response && error.response.data) {
                if (error.response.data.message == "Check-in code invalid"){
                    const checkInCodeField = document.getElementById("check-in-code-fields");
                    const invalidCodeError = document.getElementById("invalid-code");
                    checkInCodeField.classList.remove("input-primary");
                    checkInCodeField.classList.add("input-error");
                    invalidCodeError.removeAttribute("hidden")
                } else {
                    addAlert("error", error.response.data.message); // Show error message from backend
                }
            } else {
                addAlert(
                    "error",
                    "An unexpected error occurred. Please try again later."
                );
            }
        }
    }
}

const validateCheckInCode = () => {
    /**
     * Validate input in the forms
     * @return input validity in boolean
     */

        const checkInCodeField = document.getElementById("check-in-code-fields");
    var checkInCodeError = document.getElementById("code-field");
    if (checkInCode.value.length != 6) {
        checkInCodeField.classList.remove("input-primary");
        checkInCodeField.classList.add("input-error");

        checkInCodeError.removeAttribute("hidden");
        return false
    }
    return true
}

const closeModal = () => {
    const modal = document.getElementById('check-in-modal')
    modal.classList.add('opacity-0')
    setTimeout(() => { emit('close') }, 200)
};
</script>