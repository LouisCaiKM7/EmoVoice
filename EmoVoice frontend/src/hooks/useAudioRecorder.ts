import { useState, useEffect } from 'react';
import { Audio, InterruptionModeAndroid, InterruptionModeIOS } from 'expo-av';
import * as FileSystem from 'expo-file-system';

interface RecordingState {
  isRecording: boolean;
  isPaused: boolean;
  duration: number;
  uri: string | null;
}

interface UseAudioRecorderReturn {
  recordingState: RecordingState;
  startRecording: () => Promise<void>;
  stopRecording: () => Promise<string | null>;
  pauseRecording: () => Promise<void>;
  resumeRecording: () => Promise<void>;
  resetRecording: () => void;
}

export const useAudioRecorder = (): UseAudioRecorderReturn => {
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [recordingState, setRecordingState] = useState<RecordingState>({
    isRecording: false,
    isPaused: false,
    duration: 0,
    uri: null,
  });
  
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
    
    if (recordingState.isRecording && !recordingState.isPaused) {
      interval = setInterval(() => {
        setRecordingState(prev => ({
          ...prev,
          duration: prev.duration + 1,
        }));
      }, 1000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [recordingState.isRecording, recordingState.isPaused]);
  
  const startRecording = async (): Promise<void> => {
    try {
      // Reset state
      setRecordingState({
        isRecording: false,
        isPaused: false,
        duration: 0,
        uri: null,
      });
      
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
      setRecordingState(prev => ({
        ...prev,
        isRecording: true,
      }));
    } catch (err) {
      console.error('Failed to start recording', err);
    }
  };
  
  const stopRecording = async (): Promise<string | null> => {
    if (!recording) return null;
    
    try {
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      
      setRecordingState(prev => ({
        ...prev,
        isRecording: false,
        isPaused: false,
        uri,
      }));
      
      setRecording(null);
      return uri;
    } catch (err) {
      console.error('Failed to stop recording', err);
      return null;
    }
  };
  
  const pauseRecording = async (): Promise<void> => {
    if (!recording) return;
    
    try {
      await recording.pauseAsync();
      setRecordingState(prev => ({
        ...prev,
        isPaused: true,
      }));
    } catch (err) {
      console.error('Failed to pause recording', err);
    }
  };
  
  const resumeRecording = async (): Promise<void> => {
    if (!recording) return;
    
    try {
      await recording.startAsync();
      setRecordingState(prev => ({
        ...prev,
        isPaused: false,
      }));
    } catch (err) {
      console.error('Failed to resume recording', err);
    }
  };
  
  const resetRecording = (): void => {
    setRecordingState({
      isRecording: false,
      isPaused: false,
      duration: 0,
      uri: null,
    });
  };
  
  return {
    recordingState,
    startRecording,
    stopRecording,
    pauseRecording,
    resumeRecording,
    resetRecording,
  };
};