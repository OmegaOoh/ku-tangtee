import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./styles/styles.css";
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

const app = createApp(App);
app.component("VueDatePicker", VueDatePicker)
app.use(router).mount("#app");
