import React from 'react';
import { View, Text, StyleSheet, Platform } from 'react-native';
import { useTheme } from '../constants/ThemeContext';
import { Ionicons } from '@expo/vector-icons';

interface MoodSummaryProps {
  // Optional props can be added here
}

const MoodSummary: React.FC<MoodSummaryProps> = () => {
  const { theme } = useTheme();
  
  // This would typically be fetched from a state or service
  const currentMood = {
    primary: 'Joy',
    secondary: 'Calm',
    intensity: 0.8,
    timestamp: new Date(),
  };
  
  const getEmotionIcon = (emotion: string) => {
    switch(emotion.toLowerCase()) {
      case 'joy': return 'happy-outline';
      case 'sadness': return 'sad-outline';
      case 'anger': return 'flame-outline';
      case 'fear': return 'warning-outline';
      case 'surprise': return 'alert-circle-outline';
      case 'disgust': return 'remove-circle-outline';
      case 'calm': return 'water-outline';
      default: return 'help-circle-outline';
    }
  };
  
  return (
    <View style={[styles.container, { backgroundColor: theme.colors.card }]}>
      <Text style={[styles.title, { color: theme.colors.text }]}>
        Today's Mood
      </Text>
      
      <View style={styles.moodContainer}>
        <View style={[styles.iconContainer, { backgroundColor: theme.colors.joy + '30' }]}>
          <Ionicons 
            name={getEmotionIcon(currentMood.primary)} 
            size={32} 
            color={theme.colors.joy} 
          />
        </View>
        
        <View style={styles.moodDetails}>
          <Text style={[styles.primaryEmotion, { color: theme.colors.text }]}>
            {currentMood.primary}
          </Text>
          <Text style={[styles.secondaryEmotion, { color: theme.colors.textSecondary }]}>
            with hints of {currentMood.secondary}
          </Text>
          <View style={styles.intensityContainer}>
            <View 
              style={[
                styles.intensityBar, 
                { backgroundColor: theme.colors.border }
              ]}
            >
              <View 
                style={[
                  styles.intensityFill, 
                  { 
                    width: `${currentMood.intensity * 100}%`,
                    backgroundColor: theme.colors.primary 
                  }
                ]} 
              />
            </View>
            <Text style={[styles.intensityText, { color: theme.colors.textSecondary }]}>
              Intensity
            </Text>
          </View>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
      },
      android: {
        elevation: 3,
      },
    }),
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  moodContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  iconContainer: {
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  moodDetails: {
    flex: 1,
  },
  primaryEmotion: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  secondaryEmotion: {
    fontSize: 14,
    marginBottom: 8,
  },
  intensityContainer: {
    marginTop: 4,
  },
  intensityBar: {
    height: 6,
    borderRadius: 3,
    marginBottom: 4,
  },
  intensityFill: {
    height: '100%',
    borderRadius: 3,
  },
  intensityText: {
    fontSize: 12,
  },
});

export default MoodSummary;