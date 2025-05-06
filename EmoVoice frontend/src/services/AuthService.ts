import AsyncStorage from '@react-native-async-storage/async-storage';
import { User } from '../types';
import ApiService from './ApiService';

class AuthService {
  // Check if user is logged in
  async isLoggedIn(): Promise<boolean> {
    try {
      const userJson = await AsyncStorage.getItem('@user');
      return userJson !== null;
    } catch (error) {
      console.error('Error checking login status:', error);
      return false;
    }
  }
  
  // Get current user
  async getCurrentUser(): Promise<User | null> {
    try {
      const userJson = await AsyncStorage.getItem('@user');
      if (userJson) {
        return JSON.parse(userJson);
      }
      return null;
    } catch (error) {
      console.error('Error getting current user:', error);
      return null;
    }
  }
  
  // Login user
  async login(email: string, password: string): Promise<User | null> {
    try {
      // In a real app, this would call an API
      // For demo purposes, we'll simulate a successful login
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const user: User = {
        id: '123456',
        name: 'Demo User',
        email,
        preferences: {
          theme: 'light',
          notifications: true,
          shareData: false
        }
      };
      
      await AsyncStorage.setItem('@user', JSON.stringify(user));
      return user;
    } catch (error) {
      console.error('Login failed:', error);
      return null;
    }
  }
  
  // Register new user
  async register(name: string, email: string, password: string): Promise<User | null> {
    try {
      // In a real app, this would call an API
      // For demo purposes, we'll simulate a successful registration
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const user: User = {
        id: Date.now().toString(),
        name,
        email,
        preferences: {
          theme: 'light',
          notifications: true,
          shareData: false
        }
      };
      
      await AsyncStorage.setItem('@user', JSON.stringify(user));
      return user;
    } catch (error) {
      console.error('Registration failed:', error);
      return null;
    }
  }
  
  // Logout user
  async logout(): Promise<boolean> {
    try {
      await AsyncStorage.removeItem('@user');
      return true;
    } catch (error) {
      console.error('Logout failed:', error);
      return false;
    }
  }
  
  // Update user preferences
  async updatePreferences(preferences: Partial<User['preferences']>): Promise<boolean> {
    try {
      const userJson = await AsyncStorage.getItem('@user');
      if (!userJson) return false;
      
      const user: User = JSON.parse(userJson);
      user.preferences = { ...user.preferences, ...preferences };
      
      await AsyncStorage.setItem('@user', JSON.stringify(user));
      return true;
    } catch (error) {
      console.error('Error updating preferences:', error);
      return false;
    }
  }
}

export default new AuthService();