import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './styles/styles.css';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import vue3GoogleLogin from 'vue3-google-login'


const app = createApp(App);
app.component('VueDatePicker', VueDatePicker)
app.use(vue3GoogleLogin, {
    clientId: `${process.env.VUE_APP_GOOGLE_CLIENT_ID}`
})
app.use(router).mount('#app');
