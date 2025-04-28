import api from '../utils/api';
import {
  LoginCredentials,
  RegisterData,
  AuthTokens,
  User,
  PasswordResetRequest,
  PasswordResetConfirm,
  ProfileUpdate,
} from '../types/auth';

export const login = async (credentials: LoginCredentials): Promise<AuthTokens> => {
  const response = await api.post('/auth/login/', credentials);
  return response.data;
};

export const register = async (data: RegisterData): Promise<{ message: string }> => {
  const response = await api.post('/auth/register/', data);
  return response.data;
};

export const verifyEmail = async (token: string): Promise<{ message: string }> => {
  const response = await api.get(`/auth/verify-email/?token=${token}`);
  return response.data;
};

export const resendVerification = async (email: string): Promise<{ message: string }> => {
  const response = await api.post('/auth/resend-verification/', { email });
  return response.data;
};

export const getProfile = async (): Promise<User> => {
  const response = await api.get('/auth/profile/');
  return response.data;
};

export const updateProfile = async (data: ProfileUpdate): Promise<User> => {
  const response = await api.put('/auth/profile/', data);
  return response.data;
};

export const requestPasswordReset = async (data: PasswordResetRequest): Promise<{ message: string }> => {
  const response = await api.post('/auth/password-reset/', data);
  return response.data;
};

export const confirmPasswordReset = async (data: PasswordResetConfirm): Promise<{ message: string }> => {
  const response = await api.post('/auth/password-reset/confirm/', data);
  return response.data;
};

export const logout = async (): Promise<void> => {
  await api.post('/auth/logout/', { refresh: localStorage.getItem('refresh_token') });
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};