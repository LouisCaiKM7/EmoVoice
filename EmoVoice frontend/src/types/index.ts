// Define common types used across the application

// Emotion types
export type EmotionType = 'Joy' | 'Sadness' | 'Anger' | 'Fear' | 'Surprise' | 'Disgust' | 'Calm';

// Recording data structure
export interface Recording {
  id: string;
  date: string;
  duration: string;
  emotion: EmotionType;
  intensity: number;
  audioUri?: string;
}


// Mood data structure
export interface Mood {
  primary: EmotionType;
  secondary?: EmotionType;
  intensity: number;
  timestamp: Date;
}

// Report data structure
export interface Report {
  id: string;
  date: string;
  recipient: string;
  status: 'Shared' | 'Downloaded' | 'Pending';
  timeRange: 'week' | 'month' | 'custom';
  emotions: {
    [key in EmotionType]?: number[];
  };
}

// Insight data structure
export interface Insight {
  id: string;
  title: string;
  description: string;
  actionText: string;
  icon: string;
  color: string;
  category: 'trigger' | 'tip' | 'pattern';
}

// User data structure
export interface User {
  id: string;
  name: string;
  email: string;
  preferences: {
    theme: 'light' | 'dark';
    notifications: boolean;
    shareData: boolean;
  };
}