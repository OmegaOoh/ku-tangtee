import { ref } from "vue";
import apiClient from '@/api';
import { googleTokenLogin } from 'vue3-google-login';
import { createPostRequest } from './HttpRequest';


export var isAuth = ref(false);
export var fName = ref('');
export var lName = ref('');
export var pfp = ref('');

export async function login() {
    /**
     * Log user in with Google authentication token and set user data.
     * This function return nothing.
     */
    try {
        const logInResponse = await googleTokenLogin();
        if (isAuth.value) {
            await logout();
        }
        const response = await createPostRequest(
            `auth/google-oauth2/`,
            {
                access_token: logInResponse.access_token,
            },
        );
        sessionStorage.setItem('token', response.data.access);
        isAuth.value = true;
        await getUserData();
    } catch (e) {
        console.log(e);
    }
}

export async function authStatus() {
    /**
     * Check session authentication status
     * This function does not return anything.
     */
    try {
        await createPostRequest(
            `rest-auth/token/verify/`,
            {
                token: sessionStorage.getItem('token'),
            },
        );
        isAuth.value = true;
        await getUserData();
    } catch {
        isAuth.value = false;
        await logout();
    }
}

export async function logout() {
    /**
     * Logout user from the system.
     * this function return nothing.
     */
    await createPostRequest(
        `rest-auth/logout/`,
        {},
    );
    isAuth.value = false;
    sessionStorage.setItem('token', '');
}

export async function getUserData() {
    /**
     * Get user data from backend.
     * this function return nothing.
     */
    const response = await apiClient.get(`rest-auth/user/`);
    fName.value = response.data.first_name;
    lName.value = response.data.last_name;
    const profilePic = await apiClient.get(`profile-pic/`);
    pfp.value = profilePic.data.profile_picture_url;
}