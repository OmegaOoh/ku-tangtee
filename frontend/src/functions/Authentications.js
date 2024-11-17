import { ref } from 'vue';
import apiClient from '@/api';
import { googleTokenLogin } from 'vue3-google-login';
import { createPostRequest } from './HttpRequest';
import { getCookie } from './CookiesReadWrite.js';
import router from '@/router';

export var isAuth = ref(false);
export var fName = ref('');
export var lName = ref('');
export var email = ref('');
export var pfp = ref('');
export var userId = ref(-1);
export var userName = ref('');

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
        await createPostRequest(`auth/google-oauth2/`, {
            access_token: logInResponse.access_token,
        });
        isAuth.value = true;
        await getUserData();

        const profileStatus = await apiClient.get(`/profile/`);
        if (!profileStatus.data.has_profile) {
            router.push(
                `/create-profile?next=${router.currentRoute.value.path}`
            );
        }
    } catch (e) {
        console.error('error on login: ', e);
    }
}

export async function authStatus() {
    /**
     * Check session authentication status
     * This function does not return anything.
     */
    const authToken = getCookie('jwt-auth');
    const reToken = getCookie('jwt-reauth');
    if (!reToken) {
        await logout();
        return
    }
    if (!authToken && reToken) {
        await createPostRequest('rest-auth/token/refresh/', {'Refresh': reToken})
        isAuth.value = true;
        getUserData();
        return
    }
    if (authToken) {
        isAuth.value = true;
        getUserData();
        return
    }
}

export async function logout() {
    /**
     * Logout user from the system.
     * this function return nothing.
     */
    await createPostRequest(`rest-auth/logout/`, {});
    isAuth.value = false;
    fName.value = '';
    lName.value = '';
    email.value = '';
    pfp.value = '';
    userId.value = '';
    userName.value = '';
}

export async function getUserData() {
    /**
     * Get user data from backend.
     * this function return nothing.
     */
    try {
        const response = await apiClient.get(`rest-auth/user/`);
        fName.value = response.data.first_name;
        lName.value = response.data.last_name;
        email.value = response.data.email;
        userName.value = response.data.username;
        const profilePic = await apiClient.get(`profile-pic/`);
        pfp.value = profilePic.data.profile_picture_url;
        userId.value = response.data.pk;
    } catch (e) {
        console.error(e);
        await logout();
    }
}
