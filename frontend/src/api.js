import axios from 'axios';
import { getCsrfToken } from './utils/csrf';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',  // Django backend URL
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCsrfToken(),  // Include CSRF token in the header
  }
});

export default apiClient;
