<template>
    <div class='drawer h-screen'>
        <input id='my-drawer' type='checkbox' class='drawer-toggle' />
        <div class='drawer-content flex flex-col'>
            <div class='flex items-center justify-between p-4 sticky z-10 top-0 backdrop-blur-md  w-screen h-fit'>
                <label
                    for='my-drawer'
                    class='btn pl-5 btn-ghost rounded-none drawer-button w-auto h-5'
                >
                    ☰
                </label>
                <h1><RouterLink to="/">KU Tangtee</RouterLink></h1>
                <div class="pr-5">
                    <div v-if='!isAuth'>
                        <button class='btn btn-ghost rounded-none' @click='login'>
                            Login
                        </button>
                    </div>
                    <div
                        v-else
                        class='dropdown dropdown-hover dropdown-end'
                    >
                        <div tabindex="0" role="button">
                            <img
                                v-if='pfp'
                                :src='pfp'
                                alt='Profile Picture'
                                class='w-8 h-8 rounded-full mr-2'
                            />
                        </div>
                        <ul tabindex="0" class="menu dropdown-content bg-base-300 rounded-box z-20 w-52 p-2 shadow">
                            <li class="p-2"> {{ fName }} {{ lName }}</li>
                            <li @click='logout'><a>
                                Logout
                            </a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <router-view />
            <div class='z-20 fixed bottom-1 right-0 w-2/5'>
                <AlertToast
                    v-for='(alert, index) in alerts'
                    class='text-ms justify-start h-auto'
                    style='margin-top: 0.25rem;'
                    :key='index'
                    :content='alert.content'
                    :type='alert.type'
                    :isVisible='alert.isVisible'
                    @update:isVisible='hideAlert(index)'
                />
            </div>
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
import { useAlert } from './functions/AlertManager';
import AlertToast from './component/AlertToast.vue';
import { login, logout, authStatus, isAuth, pfp, fName, lName } from './functions/Authentications';

const { alerts } = useAlert();
</script>

<script>
export default {
    name: 'App',
    data() {
        return {
            isDarkTheme: false,
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
