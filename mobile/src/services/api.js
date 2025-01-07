import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const api = axios.create({
  baseURL: 'http://10.0.2.2:8000', // Android localhost
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to add auth token
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const login = async (username, password) => {
  try {
    const response = await api.post('/api/auth/login/', { username, password });
    await AsyncStorage.setItem('token', response.data.token);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const register = async (userData) => {
  try {
    const response = await api.post('/api/auth/register/', userData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getPrograms = async () => {
  try {
    const response = await api.get('/api/programs/');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getWorkouts = async () => {
  try {
    const response = await api.get('/api/workouts/');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export default api;
