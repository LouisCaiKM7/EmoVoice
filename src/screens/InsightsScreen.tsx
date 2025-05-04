import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Platform } from 'react-native';
import { useTheme } from '../constants/ThemeContext';
import EmotionChart from '../components/EmotionChart';
import InsightCard from '../components/InsightCard';
import WeeklySelector from '../components/WeeklySelector';

const InsightsScreen = () => {
  const { theme } = useTheme();
  const [selectedPeriod, setSelectedPeriod] = useState('week');
  
  return (
    <ScrollView 
      style={[styles.container, { backgroundColor: theme.colors.background }]}
      contentContainerStyle={styles.contentContainer}
    >
      <View style={styles.header}>
        <Text style={[styles.headerTitle, { color: theme.colors.text }]}>
          Your Emotional Insights
        </Text>
        <Text style={[styles.headerSubtitle, { color: theme.colors.textSecondary }]}>
          Track your emotional patterns over time
        </Text>
      </View>
      
      <View style={styles.periodSelector}>
        <TouchableOpacity 
          style={[
            styles.periodButton, 
            selectedPeriod === 'week' && { backgroundColor: theme.colors.primary }
          ]}
          onPress={() => setSelectedPeriod('week')}
        >
          <Text style={[
            styles.periodButtonText, 
            selectedPeriod === 'week' && { color: 'white' }
          ]}>Week</Text>
        </TouchableOpacity>
        <TouchableOpacity 
          style={[
            styles.periodButton, 
            selectedPeriod === 'month' && { backgroundColor: theme.colors.primary }
          ]}
          onPress={() => setSelectedPeriod('month')}
        >
          <Text style={[
            styles.periodButtonText, 
            selectedPeriod === 'month' && { color: 'white' }
          ]}>Month</Text>
        </TouchableOpacity>
      </View>
      
      <WeeklySelector />
      
      <View style={styles.chartContainer}>
        <EmotionChart period={selectedPeriod} />
      </View>
      
      <Text style={[styles.sectionTitle, { color: theme.colors.text }]}>
        Emotional Triggers
      </Text>
      
      <InsightCard 
        title="Morning Stress"
        description="Your stress levels tend to peak in the mornings around 9 AM."
        actionText="Tips to reduce morning stress"
        icon="alert-circle-outline"
        color={theme.colors.warning}
      />
      
      <InsightCard 
        title="Joy Moments"
        description="You experience more joy during evening conversations."
        actionText="Enhance your evening routine"
        icon="happy-outline"
        color={theme.colors.joy}
      />
      
      <Text style={[styles.sectionTitle, { color: theme.colors.text }]}>
        AI Coping Tips
      </Text>
      
      <InsightCard 
        title="Deep Breathing"
        description="Try 4-7-8 breathing when feeling anxious: inhale for 4 seconds, hold for 7, exhale for 8."
        actionText="Learn more techniques"
        icon="fitness-outline"
        color={theme.colors.info}
      />
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
  header: {
    marginBottom: 20,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  headerSubtitle: {
    fontSize: 16,
    marginTop: 4,
  },
  periodSelector: {
    flexDirection: 'row',
    marginBottom: 20,
  },
  periodButton: {
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 20,
    marginRight: 10,
    backgroundColor: '#E0E0E0',
  },
  periodButtonText: {
    fontWeight: '500',
  },
  chartContainer: {
    marginVertical: 20,
    height: 250,
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
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
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 24,
    marginBottom: 16,
  },
});

export default InsightsScreen;