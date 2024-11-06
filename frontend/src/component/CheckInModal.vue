<template>
    <div class="form-control w-full">
        <div class="label"> 
            <span class="text-base-content text-4xl">Check-In Code: </span>
        </div>
        <div class="label"> 
            <span id="code-field-must-6" class="text-error text-sm" hidden>
                Check-in code must have 6 characters
            </span>
            <span id="invalid-code" class="text-error text-sm" hidden>
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
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue';
import { useRoute } from 'vue-router';
import { addAlert } from "@/functions/AlertManager";
import { createPostRequest } from "@/functions/HttpRequest.js";
const emit = defineEmits(['checkInSuccess'])

const checkInCode = ref("");
const activityId = ref(null);

onMounted(() => {
    activityId.value = route.params.id;
    checkInCode.value = route.query.code;
});

const route = useRoute();
activityId.value = route.params.id;


async function postCheckIn() {
    if (validateCheckInCode()) {
        try {
            const response = await createPostRequest(
                `/activities/check-in/${activityId.value}/`,
                {
                    'check_in_code': checkInCode.value
                }
            );
            addAlert("success", response.data.message);
            emit("check-in-success");
        } catch (error) {
            handleError(error);
        }
    }
}


async function validateCheckInCode() {
    const checkInCodeField = document.getElementById("check-in-code-fields");
    const checkInCodeError = document.getElementById("code-field-must-6");
    let result = true;

    if (checkInCode.value.length !== 6) {
        checkInCodeField.classList.remove("input-primary");
        checkInCodeField.classList.add("input-error");
        checkInCodeError.removeAttribute("hidden");
        result = false;
    } else {
        checkInCodeField.classList.remove("input-error");
        checkInCodeField.classList.add("input-primary");
        checkInCodeError.setAttribute("hidden", true);
    }

    return result;
}


async function handleError(error) {
    const checkInCodeField = document.getElementById("check-in-code-fields");
    const invalidCodeError = document.getElementById("invalid-code");

    if (error.response && error.response.data) {
        if (error.response.data.message === "Check-in code invalid") {
            checkInCodeField.classList.remove("input-primary");
            checkInCodeField.classList.add("input-error");
            invalidCodeError.removeAttribute("hidden");
        } else {
            addAlert("error", error.response.data.message); // Show error message from backend
        }
    } else {
        addAlert("error", "An unexpected error occurred. Please try again later.");
    }
}
</script>