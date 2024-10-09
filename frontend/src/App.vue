<script setup>
import { googleTokenLogin } from "vue3-google-login"
import apiClient from "./api";


const login = async() => {
    const logInResponse = await googleTokenLogin()
    console.log("Google Response: ", logInResponse)
    const csrfToken = await apiClient.get(`activities/get-csrf-token/`,{})
    const response = await apiClient.post(`auth/google-oauth2/`,
        {
            access_token: logInResponse.access_token,
        },
        {
            headers: { "X-CsrfToken": csrfToken},
            withCredentials: true,
        }
    )
    console.log("Django Response: ", response)
}
</script>
<template>
    <button @click="login">Login Using Google</button>
    <div id="app">
        <router-view />
    </div>
</template>

<script>
export default {
    name: "App",
};
</script>
