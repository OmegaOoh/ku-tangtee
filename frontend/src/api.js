import axios from 'axios';
import { getCsrfToken } from './utils/csrf';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Django address that we are going to get API
  headers: {
    'Content-Type': 'application/json',
  }
});

apiClient.interceptors.request.use((config) => {
  const csrfToken = getCsrfToken();
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken; // Set CSRF token for every request
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default apiClient;
