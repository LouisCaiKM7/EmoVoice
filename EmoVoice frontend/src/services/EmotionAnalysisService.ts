import { EmotionType, Mood } from '../types';

// This would be replaced with actual ML model integration
// Currently using mock data for demonstration
class EmotionAnalysisService {
  // Analyze audio and return detected emotions
  async analyzeAudio(audioUri: string): Promise<Mood> {
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock emotion detection result
    // In a real app, this would call TensorFlow Lite model
    const emotions: EmotionType[] = ['Joy', 'Sadness', 'Anger', 'Fear', 'Surprise', 'Disgust', 'Calm'];
    const randomEmotion = emotions[Math.floor(Math.random() * emotions.length)];
    const secondaryEmotion = emotions.filter(e => e !== randomEmotion)[
      Math.floor(Math.random() * (emotions.length - 1))
    ];
    
    return {
      primary: randomEmotion,
      secondary: secondaryEmotion,
      intensity: Math.random() * 0.5 + 0.5, // Random intensity between 0.5 and 1.0
      timestamp: new Date(),
    };
  }
  
  // Get insights based on emotion history
  async getInsights(recordings: any[]): Promise<any[]> {
    // This would analyze patterns in the emotion data
    // For now, return mock insights
    return [
      {
        id: '1',
        title: 'Morning Stress',
        description: 'Your stress levels tend to peak in the mornings around 9 AM.',
        actionText: 'Tips to reduce morning stress',
        icon: 'alert-circle-outline',
        color: '#FFC107',
        category: 'trigger',
      },
      {
        id: '2',
        title: 'Joy Moments',
        description: 'You experience more joy during evening conversations.',
        actionText: 'Enhance your evening routine',
        icon: 'happy-outline',
        color: '#FFD700',
        category: 'pattern',
      },
      {
        id: '3',
        title: 'Deep Breathing',
        description: 'Try 4-7-8 breathing when feeling anxious: inhale for 4 seconds, hold for 7, exhale for 8.',
        actionText: 'Learn more techniques',
        icon: 'fitness-outline',
        color: '#17A2B8',
        category: 'tip',
      },
    ];
  }
}

export default new EmotionAnalysisService();