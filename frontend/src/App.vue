<template>
    <div class='drawer h-screen'>
        <input id='my-drawer' type='checkbox' class='drawer-toggle' />
        <div class='drawer-content flex flex-col'>
            <div class='flex items-center justify-between p-4 sticky z-10 top-0 backdrop-blur-md w-screen h-10'>
                <label
                    for='my-drawer'
                    class='btn btn-ghost drawer-button w-auto h-5'
                >
                    ☰
                </label>
                <div>
                    <div v-if='!isAuth'>
                        <button class='btn btn-ghost' @click='login'>
                            Login
                        </button>
                    </div>
                    <div
                        v-else
                        class='relative'
                        @mouseenter='showDropdown'
                        @mouseleave='hideDropdown'
                    >
                        <div
                            class='btn btn-ghost flex items-center cursor-pointer'
                        >
                            <img
                                v-if='pfp'
                                :src='pfp'
                                alt='Profile Picture'
                                class='w-8 h-8 rounded-full mr-2'
                            />
                        </div>
                        <div
                            v-if='isDropdown'
                            class='absolute right-0 w-48 bg-base-200 rounded-full shadow-lg z-10 justify-center'
                            @mouseenter='keepDropdownOpen'
                            @mouseleave='checkHideDropdown'
                        >
                            <ul>
                                <li
                                    class='block px-4 py-2 text-center hover:bg-base-300 cursor-pointer rounded-full'
                                    @click='logout'
                                >
                                    Logout
                                </li>
                            </ul>
                        </div>
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
                <li><router-link to='/'>Home</router-link></li>
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
import { login, logout, authStatus, isAuth, pfp } from './functions/Authentications';

const { alerts } = useAlert();
</script>

<script>
export default {
    name: 'App',
    data() {
        return {
            isDarkTheme: false,
            isDropdown: false,
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
    methods: {
        showDropdown() {
            /**
             * Show dropdown.
             * This function return nothing.
             */
            this.isDropdown = true;
            this.isMouseOverDropdown = true;
            clearTimeout(this.hideTimeout);
        },
        hideDropdown() {
            /**
             * Deactivate dropdown.
             * This function return nothing.
             */
            this.isDropdown = false;
            this.isMouseOverDropdown = false;
        },
        checkHideDropdown() {
            /**
             * Deactivate dropdown with timer and mouse condition.
             * This function return nothing.
             */
            if (!this.isMouseOverDropdown) {
                this.hideDropdown();
            }
        },
        startHideTimeout() {
            /**
             * This sets a timer for hiding dropdown.
             * This function returns nothing.
             */
            this.hideTimeout = setTimeout(() => {
                this.checkHideDropdown();
            }, 1000);
        },
        keepDropdownOpen() {
            /**
             * This sets a flag indicating the mouse is over the dropdown.
             * This function returns nothing.
             */
            this.isMouseOverDropdown = true;
            clearTimeout(this.hideTimeout);
        },
        navBarLogout() {
            /**
             * Logout and close the dropdown.
             * This function returns nothing.
             */
            logout();
            this.isDropdown = false;
        }
    },
};
</script>
