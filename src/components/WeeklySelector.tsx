import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useTheme } from '../constants/ThemeContext';

const WeeklySelector: React.FC = () => {
  const { theme } = useTheme();
  const [currentWeek, setCurrentWeek] = useState('Oct 15 - Oct 21');
  
  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.arrowButton}>
        <Ionicons name="chevron-back" size={24} color={theme.colors.primary} />
      </TouchableOpacity>
      
      <Text style={[styles.weekText, { color: theme.colors.text }]}>
        {currentWeek}
      </Text>
      
      <TouchableOpacity style={styles.arrowButton}>
        <Ionicons name="chevron-forward" size={24} color={theme.colors.primary} />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  arrowButton: {
    padding: 8,
  },
  weekText: {
    fontSize: 16,
    fontWeight: '500',
  },
});

export default WeeklySelector;