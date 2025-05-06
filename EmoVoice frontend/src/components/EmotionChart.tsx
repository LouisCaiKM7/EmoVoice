import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { useTheme } from '../constants/ThemeContext';
import { LineChart } from 'react-native-chart-kit';

interface EmotionChartProps {
  period: string;
}

const EmotionChart: React.FC<EmotionChartProps> = ({ period }) => {
  const { theme } = useTheme();
  
  // Mock data - would typically come from a service or state
  const weekData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        data: [0.3, 0.5, 0.7, 0.4, 0.8, 0.6, 0.9],
        color: () => theme.colors.joy,
        strokeWidth: 2,
      },
      {
        data: [0.5, 0.3, 0.2, 0.5, 0.1, 0.2, 0.1],
        color: () => theme.colors.sadness,
        strokeWidth: 2,
      },
      {
        data: [0.2, 0.1, 0.1, 0.1, 0.1, 0.2, 0.0],
        color: () => theme.colors.anger,
        strokeWidth: 2,
      },
    ],
    legend: ['Joy', 'Sadness', 'Anger'],
  };
  
  const monthData = {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    datasets: [
      {
        data: [0.6, 0.7, 0.5, 0.8],
        color: () => theme.colors.joy,
        strokeWidth: 2,
      },
      {
        data: [0.3, 0.2, 0.4, 0.1],
        color: () => theme.colors.sadness,
        strokeWidth: 2,
      },
      {
        data: [0.1, 0.1, 0.1, 0.1],
        color: () => theme.colors.anger,
        strokeWidth: 2,
      },
    ],
    legend: ['Joy', 'Sadness', 'Anger'],
  };
  
  const chartData = period === 'week' ? weekData : monthData;
  const screenWidth = Dimensions.get('window').width - 40;
  
  return (
    <View style={styles.container}>
      <Text style={[styles.title, { color: theme.colors.text }]}>
        Emotion Trends
      </Text>
      
      <LineChart
        data={chartData}
        width={screenWidth}
        height={220}
        chartConfig={{
          backgroundColor: theme.colors.card,
          backgroundGradientFrom: theme.colors.card,
          backgroundGradientTo: theme.colors.card,
          decimalPlaces: 1,
          color: (opacity = 1) => theme.colors.text,
          labelColor: (opacity = 1) => theme.colors.textSecondary,
          style: {
            borderRadius: 16,
          },
          propsForDots: {
            r: '6',
            strokeWidth: '2',
          },
        }}
        bezier
        style={styles.chart}
      />
      
      <View style={styles.legendContainer}>
        {chartData.legend.map((label, index) => (
          <View key={index} style={styles.legendItem}>
            <View 
              style={[
                styles.legendColor, 
                { 
                  backgroundColor: index === 0 
                    ? theme.colors.joy 
                    : index === 1 
                      ? theme.colors.sadness 
                      : theme.colors.anger 
                }
              ]} 
            />
            <Text style={[styles.legendText, { color: theme.colors.text }]}>
              {label}
            </Text>
          </View>
        ))}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  chart: {
    borderRadius: 16,
  },
  legendContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 16,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginHorizontal: 10,
  },
  legendColor: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 4,
  },
  legendText: {
    fontSize: 12,
  },
});

export default EmotionChart;