import React, { useState } from 'react';
import { View, Text, StyleSheet, Switch, TouchableOpacity, ScrollView, Platform } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useTheme } from '../constants/ThemeContext';

interface SettingItemProps {
  icon: string;
  title: string;
  description?: string;
  isSwitch?: boolean;
  value?: boolean;
  onValueChange?: (value: boolean) => void;
  onPress?: () => void;
}

const SettingItem: React.FC<SettingItemProps> = ({ 
  icon, 
  title, 
  description, 
  isSwitch = false, 
  value, 
  onValueChange,
  onPress,
}) => {
  const { theme } = useTheme();
  
  return (
    <TouchableOpacity 
      style={[styles.settingItem, { borderBottomColor: theme.colors.border }]}
      onPress={onPress}
      disabled={isSwitch}
    >
      <View style={[styles.iconContainer, { backgroundColor: theme.colors.primary + '20' }]}>
        <Ionicons name={icon as any} size={22} color={theme.colors.primary} />
      </View>
      <View style={styles.settingContent}>
        <Text style={[styles.settingTitle, { color: theme.colors.text }]}>{title}</Text>
        {description && (
          <Text style={[styles.settingDescription, { color: theme.colors.textSecondary }]}>
            {description}
          </Text>
        )}
      </View>
      {isSwitch ? (
        <Switch
          value={value}
          onValueChange={onValueChange}
          trackColor={{ false: '#D1D1D6', true: theme.colors.primary + '80' }}
          thumbColor={value ? theme.colors.primary : '#F4F3F4'}
        />
      ) : (
        <Ionicons name="chevron-forward" size={20} color={theme.colors.textSecondary} />
      )}
    </TouchableOpacity>
  );
};

const SettingsScreen = () => {
  const { theme, toggleTheme } = useTheme();
  const [privacySettings, setPrivacySettings] = useState({
    storeLocally: true,
    anonymizeData: true,
    shareAnalytics: false,
  });
  
  const [integrations, setIntegrations] = useState({
    smartLights: false,
    musicApps: true,
  });
  
  return (
    <ScrollView 
      style={[styles.container, { backgroundColor: theme.colors.background }]}
      contentContainerStyle={styles.contentContainer}
    >
      <Text style={[styles.sectionTitle, { color: theme.colors.text }]}>
        Privacy Controls
      </Text>
      
      <View style={[styles.settingGroup, { backgroundColor: theme.colors.card }]}>
        <SettingItem
          icon="lock-closed-outline"
          title="Store Data Locally Only"
          description="Keep all your emotional data on your device"
          isSwitch={true}
          value={privacySettings.storeLocally}
          onValueChange={(value) => 
            setPrivacySettings({...privacySettings, storeLocally: value})
          }
        />
        
        <SettingItem
          icon="eye-off-outline"
          title="Anonymize Data"
          description="Remove identifying information from your data"
          isSwitch={true}
          value={privacySettings.anonymizeData}
          onValueChange={(value) => 
            setPrivacySettings({...privacySettings, anonymizeData: value})
          }
        />
        
        <SettingItem
          icon="analytics-outline"
          title="Share Anonymous Analytics"
          description="Help improve EmoVoice with anonymous usage data"
          isSwitch={true}
          value={privacySettings.shareAnalytics}
          onValueChange={(value) => 
            setPrivacySettings({...privacySettings, shareAnalytics: value})
          }
        />
      </View>
      
      <Text style={[styles.sectionTitle, { color: theme.colors.text }]}>
        Smart Home Integrations
      </Text>
      
      <View style={[styles.settingGroup, { backgroundColor: theme.colors.card }]}>
        <SettingItem
          icon="bulb-outline"
          title="Smart Lighting"
          description="Adjust lights based on your emotional state"
          isSwitch={true}
          value={integrations.smartLights}
          onValueChange={(value) => 
            setIntegrations({...integrations, smartLights: value})
          }
        />
        
        <SettingItem
          icon="musical-notes-outline"
          title="Music Apps"
          description="Suggest playlists based on your mood"
          isSwitch={true}
          value={integrations.musicApps}
          onValueChange={(value) => 
            setIntegrations({...integrations, musicApps: value})
          }
        />
        
        <SettingItem
          icon="add-circle-outline"
          title="Connect New Device"
          onPress={() => {/* Navigate to device connection screen */}}
        />
      </View>
      
      <Text style={[styles.sectionTitle, { color: theme.colors.text }]}>
        App Settings
      </Text>
      
      <View style={[styles.settingGroup, { backgroundColor: theme.colors.card }]}>
        <SettingItem
          icon="notifications-outline"
          title="Notifications"
          onPress={() => {/* Navigate to notifications settings */}}
        />
        
        <SettingItem
          icon="moon-outline"
          title="Dark Mode"
          isSwitch={true}
          value={theme.isDark}
          onValueChange={toggleTheme}
        />
        
        <SettingItem
          icon="trash-outline"
          title="Clear All Data"
          description="Permanently delete all your recordings and analysis"
          onPress={() => {/* Show confirmation dialog */}}
        />
      </View>
      
      <View style={styles.versionContainer}>
        <Text style={[styles.versionText, { color: theme.colors.textSecondary }]}>
          EmoVoice v1.0.0
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
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 24,
    marginBottom: 8,
  },
  settingGroup: {
    borderRadius: 12,
    overflow: 'hidden',
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
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderBottomWidth: 1,
  },
  iconContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  settingContent: {
    flex: 1,
  },
  settingTitle: {
    fontSize: 16,
    fontWeight: '500',
  },
  settingDescription: {
    fontSize: 14,
    marginTop: 2,
  },
  versionContainer: {
    marginTop: 40,
    alignItems: 'center',
    paddingBottom: 20,
  },
  versionText: {
    fontSize: 14,
  },
});

export default SettingsScreen;