import React, { createContext, useState, useContext, useEffect } from 'react';
import { useColorScheme } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { COLORS, SIZES, FONTS, SHADOWS } from './theme';

type Theme = {
  colors: typeof COLORS & {
    primary: string;
    background: string;
    card: string;
    text: string;
    textSecondary: string;
    border: string;
    notification: string;
    error: string;
    success: string;
    warning: string;
    info: string;
    joy: string;
    sadness: string;
    anger: string;
    fear: string;
    surprise: string;
    disgust: string;
    calm: string;
  };
  sizes: typeof SIZES;
  fonts: typeof FONTS;
  shadows: typeof SHADOWS;
  isDark: boolean;
};

const defaultTheme: Theme = {
  colors: {
    ...COLORS,
    // Add missing properties required by the Theme type
    notification: COLORS.warning,
    error: COLORS.danger,
    calm: COLORS.secondary,
    // Make sure all required properties are present
    background: COLORS.background,
    card: COLORS.card,
    textSecondary: COLORS.textSecondary,
    border: COLORS.border
  },
  sizes: SIZES,
  fonts: FONTS,
  shadows: SHADOWS,
  isDark: false,
};

// Define theme colors
const lightTheme = {
  colors: {
    primary: '#6200EE',
    background: '#F7F7F7',
    card: '#FFFFFF',
    text: '#000000',
    textSecondary: '#757575',
    border: '#E0E0E0',
    notification: '#FF4081',
    error: '#B00020',
    success: '#4CAF50',
    warning: '#FFC107',
    info: '#2196F3',
    joy: '#FFD700',
    sadness: '#4FC3F7',
    anger: '#FF5252',
    fear: '#7E57C2',
    surprise: '#FF4081',
    disgust: '#66BB6A',
    calm: '#81D4FA',
  },
  sizes: SIZES,
  fonts: FONTS,
  shadows: SHADOWS,
  isDark: false,
};

const darkTheme = {
  colors: {
    primary: '#BB86FC',
    background: '#121212',
    card: '#1E1E1E',
    text: '#FFFFFF',
    textSecondary: '#B0B0B0',
    border: '#2C2C2C',
    notification: '#CF6679',
    error: '#CF6679',
    success: '#4CAF50',
    warning: '#FFC107',
    info: '#64B5F6',
    joy: '#FFD700',
    sadness: '#4FC3F7',
    anger: '#FF5252',
    fear: '#7E57C2',
    surprise: '#FF4081',
    disgust: '#66BB6A',
    calm: '#81D4FA',
  },
  sizes: SIZES,
  fonts: FONTS,
  shadows: SHADOWS,
  isDark: true,
};

// Create theme context
type ThemeContextType = {
  theme: typeof lightTheme;
  isDark: boolean;
  toggleTheme: () => void;
  setTheme: (scheme: 'light' | 'dark' | 'system') => void;
};

const ThemeContext = createContext<ThemeContextType>({
  theme: lightTheme,
  isDark: false,
  toggleTheme: () => {},
  setTheme: () => {},
});

// Theme provider component
export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const systemColorScheme = useColorScheme();
  const [themePreference, setThemePreference] = useState<'light' | 'dark' | 'system'>('system');
  const [isDark, setIsDark] = useState(systemColorScheme === 'dark');
  
  // Load saved theme preference
  useEffect(() => {
    const loadThemePreference = async () => {
      try {
        const savedPreference = await AsyncStorage.getItem('@theme_preference');
        if (savedPreference) {
          setThemePreference(savedPreference as 'light' | 'dark' | 'system');
          setIsDark(
            savedPreference === 'system' 
              ? systemColorScheme === 'dark' 
              : savedPreference === 'dark'
          );
        }
      } catch (error) {
        console.error('Error loading theme preference:', error);
      }
    };
    
    loadThemePreference();
  }, [systemColorScheme]);
  
  // Toggle between light and dark themes
  const toggleTheme = async () => {
    const newTheme = isDark ? 'light' : 'dark';
    setThemePreference(newTheme);
    setIsDark(!isDark);
    try {
      await AsyncStorage.setItem('@theme_preference', newTheme);
    } catch (error) {
      console.error('Error saving theme preference:', error);
    }
  };
  
  // Set specific theme
  const setTheme = async (scheme: 'light' | 'dark' | 'system') => {
    setThemePreference(scheme);
    setIsDark(
      scheme === 'system' 
        ? systemColorScheme === 'dark' 
        : scheme === 'dark'
    );
    try {
      await AsyncStorage.setItem('@theme_preference', scheme);
    } catch (error) {
      console.error('Error saving theme preference:', error);
    }
  };
  
  // Get current theme
  const theme = isDark ? darkTheme : lightTheme;
  
  return (
    <ThemeContext.Provider value={{ theme, isDark, toggleTheme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

// Custom hook for using theme
export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

// Remove the duplicate export below
