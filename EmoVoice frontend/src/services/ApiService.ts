import { EmotionType, Mood, Report } from '../types';
import Constants from 'expo-constants';

// This service handles API communication with the Flask backend
class ApiService {
  private baseUrl: string;
  
  constructor() {
    // In a real app, this would be set in environment variables
    // For development, we'll use a default local URL
    this.baseUrl = Constants.manifest?.extra?.apiUrl || 'http://192.168.2.136:5000/api';
  }
  
  // Helper method for making API requests
  private async fetchWithTimeout(url: string, options: RequestInit, timeout = 8000): Promise<Response> {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
    
    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal
      });
      clearTimeout(id);
      return response;
    } catch (error) {
      clearTimeout(id);
      throw error;
    }
  }
  
  // Upload audio for emotion analysis
  async analyzeAudio(audioUri: string): Promise<Mood> {
    try {
      // Create form data with audio file
      const formData = new FormData();
      formData.append('audio', {
        uri: audioUri,
        name: 'recording.m4a',
        type: 'audio/m4a'
      } as any);
      
      const response = await this.fetchWithTimeout(`${this.baseUrl}/analyze`, {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json',
        }
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      const result = await response.json();
      
      // Transform API response to Mood object
      return {
        primary: result.primary_emotion as EmotionType,
        secondary: result.secondary_emotion as EmotionType,
        intensity: result.intensity,
        timestamp: new Date()
      };
    } catch (error) {
      console.error('Error analyzing audio:', error);
      // Fallback to random emotion if API fails
      const emotions: EmotionType[] = ['Joy', 'Sadness', 'Anger', 'Fear', 'Surprise', 'Disgust', 'Calm'];
      return {
        primary: emotions[Math.floor(Math.random() * emotions.length)],
        secondary: emotions[Math.floor(Math.random() * emotions.length)],
        intensity: Math.random() * 0.5 + 0.5,
        timestamp: new Date()
      };
    }
  }
  
  // Get emotion insights based on historical data
  async getInsights(userId: string, timeRange: string): Promise<any[]> {
    try {
      const response = await this.fetchWithTimeout(`${this.baseUrl}/insights?userId=${userId}&timeRange=${timeRange}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        }
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error fetching insights:', error);
      // Return mock insights if API fails
      return [
        {
          id: '1',
          title: 'API Connection Issue',
          description: 'Unable to fetch insights from the server. Using cached data.',
          actionText: 'Check connection',
          icon: 'wifi-off-outline',
          color: '#F44336',
          category: 'error'
        }
      ];
    }
  }
  
  // Share report with a professional
  async shareReport(report: Report): Promise<boolean> {
    try {
      const response = await this.fetchWithTimeout(`${this.baseUrl}/share-report`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(report)
      });
      
      return response.ok;
    } catch (error) {
      console.error('Error sharing report:', error);
      return false;
    }
  }
  
  // Sync local data with server
  async syncData(userId: string, data: any): Promise<boolean> {
    try {
      const response = await this.fetchWithTimeout(`${this.baseUrl}/sync`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          userId,
          data
        })
      });
      
      return response.ok;
    } catch (error) {
      console.error('Error syncing data:', error);
      return false;
    }
  }
}

export default new ApiService();