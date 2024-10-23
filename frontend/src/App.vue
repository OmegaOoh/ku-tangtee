<template>
<NavBar>
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
</NavBar>
</template>

<script setup>
import { useAlert } from '@/functions/AlertManager';
import AlertToast from '@/component/AlertToast.vue';
import {authStatus} from '@/functions/Authentications';
import NavBar from '@/component/NavBar.vue';

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
