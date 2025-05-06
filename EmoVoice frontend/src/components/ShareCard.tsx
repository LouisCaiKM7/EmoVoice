import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Platform } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useTheme } from '../constants/ThemeContext';

interface ShareCardProps {
  date: string;
  recipient: string;
  status: 'Shared' | 'Downloaded' | 'Pending';
}

const ShareCard: React.FC<ShareCardProps> = ({ date, recipient, status }) => {
  const { theme } = useTheme();
  
  const getStatusColor = () => {
    switch(status) {
      case 'Shared': return theme.colors.success;
      case 'Downloaded': return theme.colors.info;
      case 'Pending': return theme.colors.warning;
      default: return theme.colors.textSecondary;
    }
  };
  
  const getStatusIcon = () => {
    switch(status) {
      case 'Shared': return 'checkmark-circle-outline';
      case 'Downloaded': return 'download-outline';
      case 'Pending': return 'time-outline';
      default: return 'help-circle-outline';
    }
  };
  
  return (
    <View style={[styles.container, { backgroundColor: theme.colors.card }]}>
      <View style={styles.header}>
        <Text style={[styles.date, { color: theme.colors.textSecondary }]}>
          {date}
        </Text>
        <View style={styles.statusContainer}>
          <Ionicons name={getStatusIcon()} size={16} color={getStatusColor()} />
          <Text style={[styles.status, { color: getStatusColor() }]}>
            {status}
          </Text>
        </View>
      </View>
      
      <Text style={[styles.recipient, { color: theme.colors.text }]}>
        {recipient}
      </Text>
      
      <View style={styles.footer}>
        <TouchableOpacity 
          style={[styles.button, { borderColor: theme.colors.border }]}
        >
          <Ionicons name="eye-outline" size={18} color={theme.colors.primary} />
          <Text style={[styles.buttonText, { color: theme.colors.primary }]}>
            View
          </Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={[styles.button, { borderColor: theme.colors.border }]}
        >
          <Ionicons name="share-outline" size={18} color={theme.colors.primary} />
          <Text style={[styles.buttonText, { color: theme.colors.primary }]}>
            Reshare
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
      },
      android: {
        elevation: 2,
      },
    }),
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  date: {
    fontSize: 14,
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  status: {
    fontSize: 14,
    marginLeft: 4,
  },
  recipient: {
    fontSize: 18,
    fontWeight: '500',
    marginBottom: 16,
  },
  footer: {
    flexDirection: 'row',
  },
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 20,
    borderWidth: 1,
    marginRight: 12,
  },
  buttonText: {
    fontSize: 14,
    marginLeft: 4,
  },
});

export default ShareCard;