import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./styles/styles.css";
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import vue3GoogleLogin from 'vue3-google-login'

const app = createApp(App);
app.component("VueDatePicker", VueDatePicker)
app.use(vue3GoogleLogin, {
    clientId: '<Google-Client-ID>'
})
app.use(router).mount("#app");
