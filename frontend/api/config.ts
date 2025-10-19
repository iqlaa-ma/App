import axios from 'axios';

// Base URL for your API
const BASE_URL = 'http://localhost:8000';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = getAuthToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      clearAuthToken();
      // You can redirect to login here
    }
    return Promise.reject(error);
  }
);

// Helper functions for token management
const getAuthToken = (): string | null => {
  // In a real app, you'd get this from AsyncStorage or SecureStore
  // For now, returning null - implement based on your storage solution
  return null;
};

const clearAuthToken = (): void => {
  // Clear token from storage
  // Implement based on your storage solution
};

export default apiClient;
export { BASE_URL };