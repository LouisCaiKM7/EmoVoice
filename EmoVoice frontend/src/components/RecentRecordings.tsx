import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, FlatList } from 'react-native';
import { useTheme } from '../constants/ThemeContext';
import { Ionicons } from '@expo/vector-icons';

interface Recording {
  id: string;
  date: string;
  duration: string;
  emotion: string;
  intensity: number;
}

const RecentRecordings: React.FC = () => {
  const { theme } = useTheme();
  
  // Mock data - would typically come from a state or service
  const recordings: Recording[] = [
    {
      id: '1',
      date: 'Today, 10:23 AM',
      duration: '0:32',
      emotion: 'Joy',
      intensity: 0.8,
    },
    {
      id: '2',
      date: 'Yesterday, 6:45 PM',
      duration: '1:15',
      emotion: 'Calm',
      intensity: 0.6,
    },
    {
      id: '3',
      date: 'Oct 15, 2:30 PM',
      duration: '0:45',
      emotion: 'Sadness',
      intensity: 0.7,
    },
  ];
  
  const getEmotionColor = (emotion: string): string => {
    switch(emotion.toLowerCase()) {
      case 'joy': return theme.colors.joy;
      case 'sadness': return theme.colors.sadness;
      case 'anger': return theme.colors.anger;
      case 'calm': return theme.colors.info;
      default: return theme.colors.primary;
    }
  };
  
  const getEmotionIcon = (emotion: string): string => {
    switch(emotion.toLowerCase()) {
      case 'joy': return 'happy-outline';
      case 'sadness': return 'sad-outline';
      case 'anger': return 'flame-outline';
      case 'calm': return 'water-outline';
      default: return 'help-circle-outline';
    }
  };
  
  const renderRecordingItem = ({ item }: { item: Recording }) => {
    const emotionColor = getEmotionColor(item.emotion);
    
    return (
      <TouchableOpacity 
        style={[styles.recordingItem, { borderBottomColor: theme.colors.border }]}
        onPress={() => {/* Handle recording playback */}}
      >
        <View style={[styles.emotionIcon, { backgroundColor: emotionColor + '20' }]}>
        <Ionicons name={getEmotionIcon(item.emotion) as any} size={24} color={emotionColor} />
        </View>
        
        <View style={styles.recordingInfo}>
          <Text style={[styles.recordingDate, { color: theme.colors.text }]}>
            {item.date}
          </Text>
          <Text style={[styles.recordingDuration, { color: theme.colors.textSecondary }]}>
            {item.duration}
          </Text>
        </View>
        
        <View style={styles.emotionInfo}>
          <Text style={[styles.emotionText, { color: emotionColor }]}>
            {item.emotion}
          </Text>
          <View style={styles.intensityContainer}>
            <View 
              style={[styles.intensityBar, { backgroundColor: theme.colors.border }]}
            >
              <View 
                style={[
                  styles.intensityFill, 
                  { 
                    width: `${item.intensity * 100}%`,
                    backgroundColor: emotionColor 
                  }
                ]} 
              />
            </View>
          </View>
        </View>
        
        <Ionicons name="chevron-forward" size={20} color={theme.colors.textSecondary} />
      </TouchableOpacity>
    );
  };
  
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={[styles.title, { color: theme.colors.text }]}>
          Recent Recordings
        </Text>
        <TouchableOpacity>
          <Text style={[styles.viewAllText, { color: theme.colors.primary }]}>
            View All
          </Text>
        </TouchableOpacity>
      </View>
      
      <FlatList
        data={recordings}
        keyExtractor={(item) => item.id}
        renderItem={renderRecordingItem}
        scrollEnabled={false}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  viewAllText: {
    fontSize: 14,
  },
  recordingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
  },
  emotionIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  recordingInfo: {
    flex: 1,
  },
  recordingDate: {
    fontSize: 14,
    fontWeight: '500',
  },
  recordingDuration: {
    fontSize: 12,
    marginTop: 2,
  },
  emotionInfo: {
    marginRight: 12,
    alignItems: 'flex-end',
  },
  emotionText: {
    fontSize: 14,
    fontWeight: '500',
    marginBottom: 4,
  },
  intensityContainer: {
    width: 60,
  },
  intensityBar: {
    height: 4,
    borderRadius: 2,
  },
  intensityFill: {
    height: '100%',
    borderRadius: 2,
  },
});

export default RecentRecordings;