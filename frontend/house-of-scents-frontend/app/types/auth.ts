export interface User {
    id: number;
    email: string;
    name: string;
    username?: string;
    address?: string;
    phone?: string;
  }
  
  export interface AuthTokens {
    access: string;
    refresh: string;
  }
  
  export interface LoginCredentials {
    email: string;
    password: string;
  }
  
  export interface RegisterData {
    email: string;
    username: string;
    password: string;
    name: string;
  }
  
  export interface PasswordResetRequest {
    email: string;
  }
  
  export interface PasswordResetConfirm {
    token: string;
    new_password: string;
  }
  
  export interface ProfileUpdate {
    address?: string;
    phone?: string;
  }