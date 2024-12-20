import apiClient from '@/api';
import { addAlert } from './AlertManager';

export async function getCsrfToken() {
    var csrfResponse = await apiClient.get(`/activities/get-csrf-token/`);
    return csrfResponse.data.csrfToken;
}

export async function createPostRequest(path, data) {
    /**
     * Create post request with CSRF token in its headers.
     * Return HttpResponse from post request
     */
    try {
        const csrfToken = await getCsrfToken();
        return await apiClient.post(path, data, {
            headers: { 'X-CSRFToken': csrfToken },
        });
    } catch (error) {
        if (error.response && (error.response.data.message || error.response.message)) {
            if (error.response.data) {
                addAlert("error", error.response.data.message);
            } else {
                addAlert('error', error.response.message);
            }
        }
        else  if (error.request) {
            addAlert('error', "Error Connecting to server")
        } else {
            console.log(error)
            addAlert("error", "Unexpected Error")
        }
    }

}

export async function createPutRequest(path, data) {
    /**
     * Create PUT request with CSRF token in its headers.
     * Return HttpResponse from PUT request
     */
    try {
        const csrfToken = await getCsrfToken();
        return await apiClient.put(path, data, {
            headers: { 'X-CSRFToken': csrfToken },
        });
    } catch (error) {
        if (error.response && (error.response.data.message || error.response.message)) {
            if (error.response.data) {
                addAlert("error", error.response.data.message);
            } else {
                addAlert('error', error.response.message);
            }
        }
        else if (error.request) {
            addAlert('error', "Error Connecting to server")
        } else {
            addAlert("error", "Unexpected Error")
        }
    }
}

export async function createDeleteRequest(path) {
    /**
     * Create DELETE request with CSRF token in its headers.
     * Return HttpResponse from DELETE request
     */
    try {
        const csrfToken = await getCsrfToken();
        return await apiClient.delete(path, {
            headers: { 'X-CSRFToken': csrfToken },
        });
    } catch (error) {
        if (error.response && (error.response.data.message || error.response.message)) {
            if (error.response.data) {
                addAlert("error", error.response.data.message);
            } else {
                addAlert('error', error.response.message);
            }
        }
        else if (error.request) {
            addAlert('error', "Error Connecting to server")
        } else {
            addAlert("error", "Unexpected Error")
        }
    }
}
