import { createApp } from 'vue/dist/vue.esm-bundler';
import App from './App.vue';
import router from './router';
import './styles/styles.css';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import vue3GoogleLogin from 'vue3-google-login';
import VueLazyload from 'vue3-lazyload';
import VueHighlightJS from 'vue3-highlightjs'
import 'highlight.js/styles/darcula.css' // highlight styling

const app = createApp(App);
// Register component 
app.component('VueDatePicker', VueDatePicker)

// Register Package
app.use(vue3GoogleLogin, {
    clientId: `${process.env.VUE_APP_GOOGLE_CLIENT_ID}`,
});

app.use(VueHighlightJS)

const placeholderAvatar = require('./assets/no_avatar.png');
app.use(VueLazyload, {
    preLoad: 1.3,
    error: placeholderAvatar,
    loading: placeholderAvatar,
    attempt: 3,
    log: false,
});
app.use(router).mount('#app');
