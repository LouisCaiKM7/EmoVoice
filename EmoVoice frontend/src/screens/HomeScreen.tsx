import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useTheme } from '../constants/ThemeContext';
import RecordButton from '../components/RecordButton';
import MoodSummary from '../components/MoodSummary';
import RecentRecordings from '../components/RecentRecordings';

const HomeScreen = () => {
  const { theme } = useTheme();
  const [isRecording, setIsRecording] = useState(false);
  
  const handleRecordPress = () => {
    setIsRecording(!isRecording);
    // Here you would integrate with voice recording functionality
  };
  
  const handleRecordingComplete = (uri: string) => {
    // Handle the completed recording
    console.log('Recording completed:', uri);
    // You might want to save the recording or analyze it
  };
  
  return (
    <ScrollView 
      style={[styles.container, { backgroundColor: theme.colors.background }]}
      contentContainerStyle={styles.contentContainer}
    >
      <View style={styles.welcomeSection}>
        <Text style={[styles.welcomeText, { color: theme.colors.text }]}>
          How are you feeling today?
        </Text>
        <Text style={[styles.subtitleText, { color: theme.colors.textSecondary }]}>
          Tap the button below to analyze your emotions
        </Text>
      </View>
      
      <View style={styles.recordSection}>
        <RecordButton 
          isRecording={isRecording}
          onPress={handleRecordPress}
          onRecordingComplete={handleRecordingComplete}
        />
        <Text style={[styles.recordText, { color: theme.colors.textSecondary }]}>
          {isRecording ? 'Tap to stop' : 'Tap to start recording'}
        </Text>
      </View>
      
      <MoodSummary />
      
      <View style={styles.divider} />
      
      <RecentRecordings />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  contentContainer: {
    padding: 16,
  },
  welcomeSection: {
    marginTop: 20,
    marginBottom: 30,
    alignItems: 'center',
  },
  welcomeText: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  subtitleText: {
    fontSize: 16,
    textAlign: 'center',
    marginTop: 8,
  },
  recordSection: {
    alignItems: 'center',
    marginBottom: 40,
  },
  recordText: {
    marginTop: 16,
    fontSize: 16,
  },
  divider: {
    height: 1,
    backgroundColor: '#E0E0E0',
    marginVertical: 20,
  },
});

export default HomeScreen;