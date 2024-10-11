<template>
    <div class="drawer h-screen">
        <input id="my-drawer" type="checkbox" class="drawer-toggle" />
        <div class="drawer-content flex flex-col">
            <div class="flex items-center justify-between p-4">
                <label
                    for="my-drawer"
                    class="btn btn-primary drawer-button"
                    style="width: auto; padding: 0.5rem 1rem"
                >
                    ☰
                </label>
                <div>
                    <div v-if="!isAuth">
                        <button class="btn btn-primary" @click="login">
                            Login Using Google
                        </button>
                    </div>
                    <div v-else>
                        Welcome, {{ fName }} {{ lName }}
                        <button class="btn btn-primary" @click="logout">
                            Logout
                        </button>
                    </div>
                </div>
            </div>
            <router-view />
        </div>
        <div class="drawer-side">
            <label
                for="my-drawer"
                aria-label="close sidebar"
                class="drawer-overlay"
            ></label>
            <ul class="menu bg-base-200 text-base-content w-64 p-4">
                <!-- Sidebar content here -->
                <li><router-link to="/">Home</router-link></li>
                <li>
                    <router-link to="/create">Create Activity</router-link>
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { googleTokenLogin } from "vue3-google-login";
import apiClient from "./api";
</script>

<script>
export default {
    name: "App",
    data() {
        return {
            isAuth: false,
            fName: "",
            lName: "",
            isDarkTheme: false,
        };
    },
    mounted() {
        this.authStatus();
        this.isDarkTheme = window.matchMedia(
            "(prefers-color-scheme: dark)"
        ).matches;
        window
            .matchMedia("(prefers-color-scheme: dark)")
            .addEventListener("change", (e) => {
                this.isDarkTheme = e.matches;
            });
    },
    onMounted() {
        this.authStatus();
    },
    methods: {
        async login() {
            /**
             * Log user in with Google authentication token and set user data.
             * This function return nothing.
             */
            try
            {
                const logInResponse = await googleTokenLogin()
                const csrfToken = (await apiClient.get(`activities/get-csrf-token/`,{})).data.csrfToken;
                if (this.isAuth) {            

                    await apiClient.post(
                        `rest-auth/logout/`,
                        {},
                        {
                            headers: { "X-CsrfToken": csrfToken },
                            withCredentials: true,
                        }
                    );
                }
                const response = await apiClient.post(
                    `auth/google-oauth2/`,
                    {
                        access_token: logInResponse.access_token,
                    },
                    {
                        headers: { "X-CsrfToken": csrfToken },
                        withCredentials: true,
                    }
                );
                const accessToken = response.data.access;
                sessionStorage.setItem("token", accessToken);
                this.isAuth = true;
                this.getUserData();
            } catch (e) {
                console.log(e);
            }
        },
        async authStatus() {
            /**
             * Check session authentication status
             * This function does not return anything.
             */
            try { 
                const csrfToken = (await apiClient.get(`activities/get-csrf-token/`,{})).data.csrfToken;
                await apiClient.post(`rest-auth/token/verify/`,
                    {
                        token: sessionStorage.getItem('token')
                    }, 
                    {
                        headers: {"X-CsrfToken": csrfToken},
                        withCredentials: true
                    }
                )
                this.isAuth = true;
                this.getUserData();
            }
            catch{
                this.isAuth = false;
            }
        },
        async logout() {
            /**
            * Logout user from the system.
            * this function return nothing.
            */
            const csrfToken = (await apiClient.get(`activities/get-csrf-token/`,{})).data.csrfToken;
            if (this.isAuth) {            
                await apiClient.post(
                    `rest-auth/logout/`,
                    {},
                    {
                        headers: { "X-CsrfToken": csrfToken },
                        withCredentials: true,
                    }
                );
            }
            this.isAuth = false;
            sessionStorage.setItem("token", "");
        },
        async getUserData() {
            /**
             * Get user data from backend.
             * this function return nothing.
             */
            const response = await apiClient.get(`rest-auth/user/`)
            console.log(response)
            this.fName = response.data.first_name;
            this.lName = response.data.last_name;
        },
    },
};
</script>
