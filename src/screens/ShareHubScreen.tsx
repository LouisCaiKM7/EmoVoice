import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, TextInput, Platform } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useTheme } from '../constants/ThemeContext';
import ShareCard from '../components/ShareCard';

const ShareHubScreen = () => {
  const { theme } = useTheme();
  const [recipientEmail, setRecipientEmail] = useState('');
  const [timeRange, setTimeRange] = useState('week');
  
  return (
    <ScrollView 
      style={[styles.container, { backgroundColor: theme.colors.background }]}
      contentContainerStyle={styles.contentContainer}
    >
      <View style={styles.header}>
        <Text style={[styles.headerTitle, { color: theme.colors.text }]}>
          Share Your Emotional Report
        </Text>
        <Text style={[styles.headerSubtitle, { color: theme.colors.textSecondary }]}>
          Securely share your emotional data with healthcare professionals
        </Text>
      </View>
      
      <View style={[styles.card, { backgroundColor: theme.colors.card }]}>
        <Text style={[styles.cardTitle, { color: theme.colors.text }]}>
          Generate Report
        </Text>
        
        <View style={styles.inputContainer}>
          <Text style={[styles.inputLabel, { color: theme.colors.text }]}>
            Recipient Email (Optional)
          </Text>
          <TextInput
            style={[styles.input, { 
              borderColor: theme.colors.border,
              color: theme.colors.text,
            }]}
            placeholder="therapist@example.com"
            placeholderTextColor={theme.colors.textSecondary}
            value={recipientEmail}
            onChangeText={setRecipientEmail}
            keyboardType="email-address"
          />
        </View>
        
        <Text style={[styles.inputLabel, { color: theme.colors.text }]}>
          Time Range
        </Text>
        <View style={styles.timeRangeContainer}>
          {['week', 'month', 'custom'].map((range) => (
            <TouchableOpacity
              key={range}
              style={[
                styles.timeRangeButton,
                timeRange === range && { 
                  backgroundColor: theme.colors.primary,
                  borderColor: theme.colors.primary,
                }
              ]}
              onPress={() => setTimeRange(range)}
            >
              <Text style={[
                styles.timeRangeText,
                timeRange === range && { color: 'white' }
              ]}>
                {range.charAt(0).toUpperCase() + range.slice(1)}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
        
        <TouchableOpacity 
          style={[styles.generateButton, { backgroundColor: theme.colors.primary }]}
        >
          <Text style={styles.generateButtonText}>Generate Report</Text>
        </TouchableOpacity>
      </View>
      
      <Text style={[styles.sectionTitle, { color: theme.colors.text }]}>
        Recent Reports
      </Text>
      
      <ShareCard 
        date="October 15, 2023"
        recipient="Dr. Sarah Johnson"
        status="Shared"
      />
      
      <ShareCard 
        date="September 28, 2023"
        recipient="Personal Copy"
        status="Downloaded"
      />
      
      <View style={styles.securityNote}>
        <Ionicons name="shield-checkmark-outline" size={24} color={theme.colors.success} />
        <Text style={[styles.securityText, { color: theme.colors.textSecondary }]}>
          All reports are encrypted and anonymized to protect your privacy
        </Text>
      </View>
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
  card: {
    borderRadius: 12,
    padding: 16,
    marginBottom: 24,
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
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  inputContainer: {
    marginBottom: 16,
  },
  inputLabel: {
    fontSize: 16,
    marginBottom: 8,
  },
  input: {
    height: 48,
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 12,
    fontSize: 16,
  },
  timeRangeContainer: {
    flexDirection: 'row',
    marginBottom: 24,
  },
  timeRangeButton: {
    flex: 1,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E0E0E0',
    marginRight: 8,
    borderRadius: 8,
  },
  timeRangeText: {
    fontWeight: '500',
  },
  generateButton: {
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
  },
  generateButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  securityNote: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 24,
    padding: 16,
    backgroundColor: 'rgba(40, 167, 69, 0.1)',
    borderRadius: 8,
  },
  securityText: {
    flex: 1,
    marginLeft: 12,
    fontSize: 14,
  },
});

export default ShareHubScreen;