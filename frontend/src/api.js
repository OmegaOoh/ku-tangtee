import axios from "axios";

axios.defaults.withCredentials = true;
axios.defaults.xsrfHeaderName = "x-csrftoken";
axios.defaults.xsrfCookieName = "csrfToken";

const apiClient = axios.create({
    baseURL: process.env.VUE_APP_BASE_URL, // Django backend URL
});

export default apiClient;
