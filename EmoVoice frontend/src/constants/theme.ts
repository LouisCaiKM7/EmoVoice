import { Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');

export const COLORS = {
  // Base colors
  primary: '#6200EE',
  secondary: '#03DAC6',
  
  // Emotion colors
  joy: '#FFD700',
  sadness: '#4682B4',
  anger: '#FF4500',
  fear: '#800080',
  surprise: '#FF69B4',
  disgust: '#006400',
  
  // UI colors
  success: '#28A745',
  info: '#17A2B8',
  warning: '#FFC107',
  danger: '#DC3545',
  
  // Neutral colors
  text: '#212121',
  textSecondary: '#757575',
  background: '#F5F5F5',
  card: '#FFFFFF',
  border: '#E0E0E0',
  
  // Dark mode colors
  darkPrimary: '#BB86FC',
  darkBackground: '#121212',
  darkCard: '#1E1E1E',
  darkText: '#E0E0E0',
  darkTextSecondary: '#A0A0A0',
  darkBorder: '#333333',
};

export const SIZES = {
  // Global sizes
  base: 8,
  small: 12,
  medium: 16,
  large: 18,
  xlarge: 24,
  xxlarge: 32,
  
  // Font sizes
  h1: 30,
  h2: 24,
  h3: 18,
  h4: 16,
  body1: 16,
  body2: 14,
  body3: 12,
  
  // App dimensions
  width,
  height,
};

export const FONTS = {
  h1: {
    fontSize: SIZES.h1,
    fontWeight: 'bold',
  },
  h2: {
    fontSize: SIZES.h2,
    fontWeight: 'bold',
  },
  h3: {
    fontSize: SIZES.h3,
    fontWeight: '600',
  },
  h4: {
    fontSize: SIZES.h4,
    fontWeight: '600',
  },
  body1: {
    fontSize: SIZES.body1,
  },
  body2: {
    fontSize: SIZES.body2,
  },
  body3: {
    fontSize: SIZES.body3,
  },
};

export const SHADOWS = {
  small: {
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  medium: {
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.15,
    shadowRadius: 5,
    elevation: 4,
  },
  large: {
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 6,
    },
    shadowOpacity: 0.2,
    shadowRadius: 7,
    elevation: 6,
  },
};