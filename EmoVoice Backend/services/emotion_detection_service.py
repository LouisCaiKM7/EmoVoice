import os
import numpy as np
import librosa
import tensorflow as tf
from tensorflow.lite.python.interpreter import Interpreter
import soundfile as sf

class EmotionDetectionService:
    def __init__(self):
        # Path to TensorFlow Lite model
        self.model_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'models',
            'emotion_model.tflite'
        )
        
        # Ensure model directory exists
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        # Load model if it exists, otherwise use fallback
        if os.path.exists(self.model_path):
            self.interpreter = Interpreter(model_path=self.model_path)
            self.interpreter.allocate_tensors()
            
            # Get input and output details
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            self.model_loaded = True
        else:
            print("Warning: Emotion detection model not found. Using fallback method.")
            self.model_loaded = False
        
        # Define emotion labels
        self.emotions = ['Anger', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Calm']
    
    def extract_features(self, audio_path, max_pad_len=174):
        """
        Extract MFCC features from audio file
        """
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=22050)
            
            # Trim silence
            y, _ = librosa.effects.trim(y, top_db=25)
            
            # Extract duration
            duration = librosa.get_duration(y=y, sr=sr)
            
            # Extract MFCCs
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            
            # Pad or truncate to fixed length
            pad_width = max_pad_len - mfccs.shape[1]
            if pad_width > 0:
                mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
            else:
                mfccs = mfccs[:, :max_pad_len]
            
            return mfccs, duration
        
        except Exception as e:
            print(f"Error extracting features: {e}")
            return None, 0
    
    def analyze_audio(self, audio_path):
        """
        Analyze audio file and detect emotions
        """
        # Extract features
        features, duration = self.extract_features(audio_path)
        
        if features is None:
            return {
                'primary_emotion': 'Calm',
                'confidence': 0.5,
                'intensity': 0.5,
                'duration': 0
            }
        
        if self.model_loaded:
            # Prepare input data
            input_data = np.expand_dims(features, axis=0).astype(np.float32)
            
            # If model expects different shape, reshape accordingly
            if len(self.input_details[0]['shape']) == 4:
                input_data = np.expand_dims(input_data, axis=-1)
            
            # Set input tensor
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            
            # Run inference
            self.interpreter.invoke()
            
            # Get output tensor
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
            
            # Get predicted emotion
            predicted_class = np.argmax(output_data)
            confidence = float(output_data[0][predicted_class])
            
            # Get secondary emotion
            output_data_copy = output_data.copy()
            output_data_copy[0][predicted_class] = -1  # Exclude primary emotion
            secondary_class = np.argmax(output_data_copy)
            secondary_confidence = float(output_data[0][secondary_class])
            
            # Calculate intensity based on audio energy
            intensity = self.calculate_intensity(audio_path)
            
            return {
                'primary_emotion': self.emotions[predicted_class],
                'secondary_emotion': self.emotions[secondary_class],
                'confidence': confidence,
                'secondary_confidence': secondary_confidence,
                'intensity': intensity,
                'duration': duration
            }
        else:
            # Fallback method using audio features
            return self.fallback_emotion_detection(audio_path, features, duration)
    
    def fallback_emotion_detection(self, audio_path, features, duration):
        """
        Fallback method for emotion detection when model is not available
        Uses basic audio features to estimate emotions
        """
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=22050)
            
            # Extract features
            # Spectral centroid - brightness of sound
            centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
            
            # Spectral contrast - difference between peaks and valleys
            contrast = librosa.feature.spectral_contrast(y=y, sr=sr).mean()
            
            # RMS energy - volume/intensity
            rms = librosa.feature.rms(y=y).mean()
            
            # Zero crossing rate - noisiness
            zcr = librosa.feature.zero_crossing_rate(y).mean()
            
            # Tempo
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            
            # Simple rule-based classification
            # High energy, high tempo -> Joy/Anger
            # Low energy, low tempo -> Sadness/Calm
            # High contrast, high zcr -> Surprise/Fear
            # Low contrast, high centroid -> Disgust
            
            # Normalize values
            rms_norm = min(rms * 10, 1.0)  # Energy
            tempo_norm = min(tempo / 180.0, 1.0)  # Tempo
            zcr_norm = min(zcr * 100, 1.0)  # Noisiness
            
            # Simple scoring system
            scores = {
                'Anger': rms_norm * 0.8 + zcr_norm * 0.2,
                'Joy': rms_norm * 0.6 + tempo_norm * 0.4,
                'Sadness': (1 - rms_norm) * 0.7 + (1 - tempo_norm) * 0.3,
                'Fear': zcr_norm * 0.6 + (1 - rms_norm) * 0.4,
                'Surprise': zcr_norm * 0.7 + tempo_norm * 0.3,
                'Disgust': (1 - zcr_norm) * 0.5 + centroid * 0.5,
                'Calm': (1 - zcr_norm) * 0.8 + (1 - rms_norm) * 0.2
            }
            
            # Get primary and secondary emotions
            sorted_emotions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            primary_emotion = sorted_emotions[0][0]
            secondary_emotion = sorted_emotions[1][0]
            
            # Calculate intensity based on audio energy
            intensity = self.calculate_intensity(audio_path)
            
            return {
                'primary_emotion': primary_emotion,
                'secondary_emotion': secondary_emotion,
                'confidence': sorted_emotions[0][1],
                'secondary_confidence': sorted_emotions[1][1],
                'intensity': intensity,
                'duration': duration
            }
        
        except Exception as e:
            print(f"Error in fallback emotion detection: {e}")
            return {
                'primary_emotion': 'Calm',
                'confidence': 0.5,
                'intensity': 0.5,
                'duration': duration
            }
    
    def calculate_intensity(self, audio_path):
        """
        Calculate emotional intensity based on audio energy
        """
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=22050)
            
            # Calculate RMS energy
            rms = librosa.feature.rms(y=y).mean()
            
            # Normalize to 0-1 range (empirically determined thresholds)
            intensity = min(rms * 10, 1.0)
            
            return float(intensity)
        
        except Exception as e:
            print(f"Error calculating intensity: {e}")
            return 0.5