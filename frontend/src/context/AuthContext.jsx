import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);
  const [availableAccounts, setAvailableAccounts] = useState([]);

  const fetchProfile = async (explicitUserId = null) => {
    try {
      const data = await api.getProfile();
      setProfile(data);
      if (data && data.name) {
        setUser(prev => ({
          ...(prev || {}),
          id: data.id,
          name: data.name,
          email: data.email,
          target_job_role: data.target_job_role,
          overall_skill_level: data.overall_skill_level,
          education_level: data.education_level,
          experience_level: data.experience_level
        }));
      }
      return data;
    } catch (err) {
      console.warn('Could not fetch user profile:', err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  const fetchAvailableAccounts = async () => {
    try {
      const data = await api.getDemoAccounts();
      if (data && data.accounts) {
        setAvailableAccounts(data.accounts);
      }
    } catch (err) {
      console.warn('Could not fetch available accounts:', err);
    }
  };

  useEffect(() => {
    const savedId = localStorage.getItem('user_id');
    const token = localStorage.getItem('token');

    if (savedId) {
      api.setUserId(savedId);
      fetchProfile().then((p) => {
        if (!p) {
          // If saved user could not be loaded, clear stale session
          api.clearAuth();
          setUser(null);
        }
      });
    } else {
      setLoading(false);
      setUser(null);
    }

    fetchAvailableAccounts();
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const res = await api.login(email, password);
      if (res && res.user) {
        setUser(res.user);
        api.setUserId(res.user.id);
        localStorage.setItem('user_id', String(res.user.id));
        if (res.token) {
          localStorage.setItem('token', res.token);
        }
        await fetchProfile(res.user.id);
        return res;
      }
      throw new Error(res?.error || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    setLoading(true);
    try {
      const res = await api.register(userData);
      if (res && res.user) {
        setUser(res.user);
        api.setUserId(res.user.id);
        localStorage.setItem('user_id', String(res.user.id));
        if (res.token) {
          localStorage.setItem('token', res.token);
        }
        await fetchProfile(res.user.id);
        await fetchAvailableAccounts();
        return res;
      }
      throw new Error(res?.error || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    api.clearAuth();
    setUser(null);
    setProfile(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        profile,
        loading,
        isAuthenticated: Boolean(user),
        availableAccounts,
        login,
        register,
        logout,
        refreshProfile: fetchProfile,
        refreshAccounts: fetchAvailableAccounts
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
