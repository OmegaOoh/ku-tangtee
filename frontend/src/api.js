import axios from "axios";

axios.defaults.withCredentials = true;
axios.defaults.xsrfHeaderName = "x-csrftoken";
axios.defaults.xsrfCookieName = "csrfToken";

const apiClient = axios.create({
    baseURL: "http://127.0.0.1:8000", // Django backend URL
});

export default apiClient;
