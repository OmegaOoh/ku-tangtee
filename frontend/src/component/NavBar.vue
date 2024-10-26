<template>
    <div class='drawer h-screen'>
        <input id='my-drawer' type='checkbox' class='drawer-toggle' />
        <div class='drawer-content flex flex-col'>
            <div class='flex items-center p-2 sticky z-10 top-0 left-0 right-0 justify-between bg-base-300 w-screen h-fit border-b-2 border-primary backdrop-blur-md bg-opacity-50 '>
                <div class="flex justify-start items-center">
                    <label
                        v-if="isAuth"
                        for='my-drawer'
                        class='btn btn-ghost rounded-none drawer-button w-auto h-5'
                    >
                        ☰
                    </label>
                    <p class="flex items-center justify-center mx-2"><RouterLink to="/">KU Tangtee</RouterLink></p>
                </div>
                <div class="pr-5">
                    <div v-if='!isAuth'>
                        <button class='btn btn-ghost rounded-none' @click='login'>
                            Login
                        </button>
                    </div>
                    <div
                        v-else
                        id="profile-dropdown"
                        class='dropdown dropdown-end'
                    >
                        <div tabindex="0" role="button"                         
                            >
                            <img
                                v-if='pfp'
                                v-lazy='pfp'
                                alt='Profile Picture'
                                class='w-8 h-8 rounded-full mr-2 transition-all duration-100 hover:border-opacity-10 hover:border-4'
                            />
                        </div>
                        <ul
                            tabindex="0" class="menu dropdown-content bg-base-300 rounded-box z-20 w-52 p-2 shadow"
                        >
                            <li class="p-2"> {{ fName }} {{ lName }}</li>
                            <li @click='logout'><a>
                                Logout
                            </a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <slot><!--Slot Outlet--></slot>
        </div>
        <div class='drawer-side'>
            <label
                for='my-drawer'
                aria-label='close sidebar'
                class='drawer-overlay'
            ></label>
            <ul class='menu bg-base-200 text-base-content w-64 p-4'>
                <!-- Sidebar content here -->
                <li>
                    <router-link to='/create'>Create Activity</router-link>
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { login, logout, authStatus, isAuth, pfp, fName, lName } from '@/functions/Authentications';
</script>

<script>
export default {
    name: 'App',
    data() {
        return {
            isDarkTheme: false,
            closeDelay: null
        };
    },
    mounted() {
        authStatus();
        this.isDarkTheme = window.matchMedia(
            '(prefers-color-scheme: dark)'
        ).matches;
        window
            .matchMedia('(prefers-color-scheme: dark)')
            .addEventListener('change', (e) => {
                this.isDarkTheme = e.matches;
            });
    },
};
</script>
