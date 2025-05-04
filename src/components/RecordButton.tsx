import React, { useState, useEffect } from 'react';
import { 
  View, 
  TouchableOpacity, 
  StyleSheet, 
  Animated, 
  Text,
  ActivityIndicator,
  Platform
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Audio, InterruptionModeAndroid, InterruptionModeIOS } from 'expo-av';
import { useTheme } from '../constants/ThemeContext';

interface RecordButtonProps {
  onRecordingComplete: (uri: string) => void;
  isRecording?: boolean;
  onPress?: () => void;
  size?: number;
}

const RecordButton: React.FC<RecordButtonProps> = ({ 
  onRecordingComplete = () => {},
  isRecording: externalIsRecording,
  onPress,
  size = 80 
}) => {
  const { theme } = useTheme();
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  
  // Use external isRecording state if provided
  useEffect(() => {
    if (externalIsRecording !== undefined) {
      setIsRecording(externalIsRecording);
    }
  }, [externalIsRecording]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [recordingDuration, setRecordingDuration] = useState(0);
  
  // Animation values
  const pulseAnim = React.useRef(new Animated.Value(1)).current;
  const buttonScale = React.useRef(new Animated.Value(1)).current;
  
  // Request permissions
  useEffect(() => {
    (async () => {
      const { status } = await Audio.requestPermissionsAsync();
      if (status !== 'granted') {
        console.error('Permission to access microphone was denied');
      }
    })();
  }, []);
  
  // Timer for recording duration
  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (isRecording) {
      interval = setInterval(() => {
        setRecordingDuration(prev => prev + 1);
      }, 1000);
    } else {
      setRecordingDuration(0);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isRecording]);
  
  // Pulse animation when recording
  useEffect(() => {
    let pulseAnimation: Animated.CompositeAnimation;
    
    if (isRecording) {
      pulseAnimation = Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 1.2,
            duration: 800,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 800,
            useNativeDriver: true,
          }),
        ])
      );
      
      pulseAnimation.start();
    } else {
      pulseAnim.setValue(1);
    }
    
    return () => {
      if (pulseAnimation) pulseAnimation.stop();
    };
  }, [isRecording, pulseAnim]);
  
  const startRecording = async () => {
    try {
      // Configure audio
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
        staysActiveInBackground: true,
        interruptionModeIOS: InterruptionModeIOS.DoNotMix,
        interruptionModeAndroid: InterruptionModeAndroid.DoNotMix,
      });
      
      // Start recording
      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      
      setRecording(recording);
      setIsRecording(true);
      
      // Button press animation
      Animated.sequence([
        Animated.timing(buttonScale, {
          toValue: 0.9,
          duration: 100,
          useNativeDriver: true,
        }),
        Animated.timing(buttonScale, {
          toValue: 1,
          duration: 100,
          useNativeDriver: true,
        }),
      ]).start();
      
    } catch (err) {
      console.error('Failed to start recording', err);
    }
  };
  
  const stopRecording = async () => {
    if (!recording) return;
    
    // Button press animation
    Animated.sequence([
      Animated.timing(buttonScale, {
        toValue: 0.9,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(buttonScale, {
        toValue: 1,
        duration: 100,
        useNativeDriver: true,
      }),
    ]).start();
    
    setIsRecording(false);
    setIsProcessing(true);
    
    try {
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      
      if (uri) {
        // Simulate processing time (replace with actual emotion analysis)
        setTimeout(() => {
          onRecordingComplete(uri);
          setIsProcessing(false);
        }, 1500);
      } else {
        setIsProcessing(false);
      }
    } catch (err) {
      console.error('Failed to stop recording', err);
      setIsProcessing(false);
    }
    
    setRecording(null);
  };
  
  const formatDuration = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };
  
  return (
    <View style={styles.container}>
      {isRecording && (
        <Text style={[styles.durationText, { color: theme.colors.primary }]}>
          {formatDuration(recordingDuration)}
        </Text>
      )}
      
      <Animated.View 
        style={[
          styles.pulseContainer,
          { 
            transform: [{ scale: pulseAnim }],
            backgroundColor: theme.colors.primary + '20',
          }
        ]}
      />
      
      <Animated.View
        style={[
          styles.buttonContainer,
          { transform: [{ scale: buttonScale }] }
        ]}
      >
        <TouchableOpacity
          style={[
            styles.button,
            { 
              backgroundColor: isRecording ? theme.colors.error : theme.colors.primary,
              width: size,
              height: size,
              borderRadius: size / 2,
            }
          ]}
          onPress={isRecording ? stopRecording : startRecording}
          disabled={isProcessing}
        >
          {isProcessing ? (
            <ActivityIndicator color="#fff" size="large" />
          ) : (
            <Ionicons
              name={isRecording ? "square" : "mic"}
              size={size / 2.5}
              color="#fff"
            />
          )}
        </TouchableOpacity>
      </Animated.View>
      
      {!isRecording && !isProcessing && (
        <Text style={[styles.hintText, { color: theme.colors.textSecondary }]}>
          Tap to record your voice
        </Text>
      )}
      
      {isProcessing && (
        <Text style={[styles.hintText, { color: theme.colors.primary }]}>
          Analyzing emotions...
        </Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 2,
  },
  button: {
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  pulseContainer: {
    position: 'absolute',
    width: 100,
    height: 100,
    borderRadius: 50,
    zIndex: 1,
  },
  durationText: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  hintText: {
    marginTop: 16,
    fontSize: 14,
  }
});

export default RecordButton;