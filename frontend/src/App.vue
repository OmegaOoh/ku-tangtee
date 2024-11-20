<template>
    <NavBar>
        <router-view />
        <div class="z-50 fixed bottom-1 right-0 w-2/5 pointer-events-none">
            <AlertToast
                v-for="(alert, index) in alerts"
                class="text-ms justify-start h-auto"
                style="margin-top: 0.25rem"
                :key="index"
                :content="alert.content"
                :type="alert.type"
                :isVisible="alert.isVisible"
                @update:isVisible="hideAlert(index)"
            />
        </div>
    </NavBar>
</template>

<script setup>
import { useAlert } from '@/functions/AlertManager';
import AlertToast from '@/component/AlertToast.vue';
import { authStatus } from '@/functions/Authentications';
import NavBar from '@/component/NavBar.vue';

const { alerts } = useAlert();
</script>

<script>
export default {
    name: 'App',
    mounted() {
        authStatus();
    }
};
</script>
