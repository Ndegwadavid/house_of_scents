'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { User, AuthTokens } from '../types/auth';
import { getProfile } from '../api/auth';
import toast from 'react-hot-toast';

interface AuthContextType {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  login: (tokens: AuthTokens) => void;
  logout: () => void;
  setUser: (user: User | null) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [tokens, setTokens] = useState<AuthTokens | null>(null);

  useEffect(() => {
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');
    if (accessToken && refreshToken) {
      setTokens({ access: accessToken, refresh: refreshToken });
      fetchProfile();
    }
  }, []);

  const fetchProfile = async () => {
    try {
      const profile = await getProfile();
      setUser(profile);
    } catch (error) {
      toast.error('Failed to fetch profile');
      logout();
    }
  };

  const login = (newTokens: AuthTokens) => {
    localStorage.setItem('access_token', newTokens.access);
    localStorage.setItem('refresh_token', newTokens.refresh);
    setTokens(newTokens);
    fetchProfile();
  };

  const logout = () => {
    setUser(null);
    setTokens(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    toast.success('Logged out successfully');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        tokens,
        isAuthenticated: !!user && !!tokens,
        login,
        logout,
        setUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};