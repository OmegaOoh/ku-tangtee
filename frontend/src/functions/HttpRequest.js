import apiClient from '@/api';
import { authStatus, isAuth } from './Authentications';

export async function getCsrfToken() {
    var csrfResponse = await apiClient.get(`/activities/get-csrf-token/`);
    return csrfResponse.data.csrfToken;
}

export async function createPostRequest(path, data) {
    /**
     * Create post request with CSRF token in its headers.
     * Return HttpResponse from post request
     */
    await authStatus();
    if (!isAuth.value) return; 
    const csrfToken = await getCsrfToken();
    return await apiClient.post(path, data, {
        headers: { 'X-CSRFToken': csrfToken },
    });
}

export async function createPutRequest(path, data) {
    /**
     * Create PUT request with CSRF token in its headers.
     * Return HttpResponse from PUT request
     */
    await authStatus();
    if (!isAuth.value) return; 
    const csrfToken = await getCsrfToken();
    return await apiClient.put(path, data, {
        headers: { 'X-CSRFToken': csrfToken },
    });
}

export async function createDeleteRequest(path) {
    /**
     * Create DELETE request with CSRF token in its headers.
     * Return HttpResponse from DELETE request
     */
    await authStatus();
    if (!isAuth.value) return; 
    const csrfToken = await getCsrfToken();
    return await apiClient.delete(path, {
        headers: { 'X-CSRFToken': csrfToken },
    });
}
