import os
import numpy as np
import librosa
import joblib
import soundfile as sf

class EmotionDetectionService:
    def __init__(self):
        # Path to scikit-learn model
        self.model_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'models',
            'emotion_model.joblib'
        )
        
        # Ensure model directory exists
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        # Load model if it exists, otherwise use fallback
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.model_loaded = True
        else:
            print("Warning: Emotion detection model not found. Using fallback method.")
            self.model_loaded = False
        
        # Define emotion labels
        self.emotions = ['Anger', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Calm']
        
        # Enhanced feature extraction parameters
        self.sample_rate = 22050
        self.n_mfcc = 13
        self.n_fft = 2048
        self.hop_length = 512
        self.max_pad_len = 174
    
    def extract_features(self, audio_path, max_pad_len=174):
        """
        Extract MFCC features from audio file with enhanced parameters
        """
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Trim silence
            y, _ = librosa.effects.trim(y, top_db=25)
            
            # Extract duration
            duration = librosa.get_duration(y=y, sr=sr)
            
            # Extract MFCCs with enhanced parameters
            mfccs = librosa.feature.mfcc(
                y=y, 
                sr=sr, 
                n_mfcc=self.n_mfcc,
                n_fft=self.n_fft,
                hop_length=self.hop_length
            )
            
            # Extract additional features for enhanced detection
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
            spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
            
            # Normalize features
            mfccs = self._normalize_features(mfccs)
            spectral_centroid = self._normalize_features(spectral_centroid)
            spectral_contrast = self._normalize_features(spectral_contrast)
            spectral_rolloff = self._normalize_features(spectral_rolloff)
            
            # Pad or truncate to fixed length
            pad_width = max_pad_len - mfccs.shape[1]
            if pad_width > 0:
                mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
            else:
                mfccs = mfccs[:, :max_pad_len]
            
            # Flatten features for scikit-learn model
            flattened_features = mfccs.reshape(1, -1)
            
            return flattened_features, duration, {
                'spectral_centroid': spectral_centroid.mean(),
                'spectral_contrast': spectral_contrast.mean(),
                'spectral_rolloff': spectral_rolloff.mean()
            }
        
        except Exception as e:
            print(f"Error extracting features: {e}")
            return None, 0, {}
    
    def _normalize_features(self, features):
        """
        Normalize features to zero mean and unit variance
        """
        mean = features.mean(axis=1, keepdims=True)
        std = features.std(axis=1, keepdims=True) + 1e-10  # Avoid division by zero
        return (features - mean) / std
    
    def analyze_audio(self, audio_path):
        """
        Analyze audio file and detect emotions with enhanced approach
        """
        # Extract features with additional spectral features
        features, duration, spectral_features = self.extract_features(audio_path)
        
        if features is None:
            return {
                'primary_emotion': 'Calm',
                'confidence': 0.5,
                'intensity': 0.5,
                'duration': 0
            }
        
        if self.model_loaded:
            # Use scikit-learn model for prediction
            prediction_probs = self.model.predict_proba(features)
            
            # Get predicted emotion
            predicted_class = np.argmax(prediction_probs[0])
            confidence = float(prediction_probs[0][predicted_class])
            
            # Get secondary emotion
            prediction_probs_copy = prediction_probs[0].copy()
            prediction_probs_copy[predicted_class] = -1  # Exclude primary emotion
            secondary_class = np.argmax(prediction_probs_copy)
            secondary_confidence = float(prediction_probs[0][secondary_class])
            
            # Calculate intensity based on audio energy and spectral features
            intensity = self.calculate_enhanced_intensity(audio_path, spectral_features)
            
            # Apply confidence boosting based on spectral features
            confidence = self._adjust_confidence(confidence, self.emotions[predicted_class], spectral_features)
            secondary_confidence = self._adjust_confidence(secondary_confidence, self.emotions[secondary_class], spectral_features)
            
            return {
                'primary_emotion': self.emotions[predicted_class],
                'secondary_emotion': self.emotions[secondary_class],
                'confidence': confidence,
                'secondary_confidence': secondary_confidence,
                'intensity': intensity,
                'duration': duration,
                'spectral_features': spectral_features
            }
        else:
            # Enhanced fallback method using audio features
            return self.enhanced_fallback_emotion_detection(audio_path, features, duration, spectral_features)
    
    def _adjust_confidence(self, confidence, emotion, spectral_features):
        """
        Adjust confidence based on spectral features and emotion
        """
        # Adjust confidence based on spectral features for specific emotions
        centroid = spectral_features['spectral_centroid']
        contrast = spectral_features['spectral_contrast']
        rolloff = spectral_features['spectral_rolloff']
        
        # Apply emotion-specific adjustments
        if emotion == 'Anger' and contrast > 0.6:
            confidence = min(confidence * 1.2, 1.0)
        elif emotion == 'Joy' and centroid > 0.5 and rolloff > 0.6:
            confidence = min(confidence * 1.15, 1.0)
        elif emotion == 'Sadness' and centroid < 0.4 and contrast < 0.4:
            confidence = min(confidence * 1.25, 1.0)
        elif emotion == 'Fear' and rolloff > 0.7:
            confidence = min(confidence * 1.1, 1.0)
        
        return confidence
    
    def enhanced_fallback_emotion_detection(self, audio_path, features, duration, spectral_features):
        """
        Enhanced fallback method for emotion detection when model is not available
        Uses advanced audio features to estimate emotions
        """
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Extract additional features
            # Chroma features - related to the 12 different pitch classes
            chroma = librosa.feature.chroma_stft(y=y, sr=sr).mean()
            
            # Mel spectrogram
            mel = librosa.feature.melspectrogram(y=y, sr=sr)
            mel_mean = mel.mean()
            mel_std = mel.std()
            
            # RMS energy - volume/intensity
            rms = librosa.feature.rms(y=y).mean()
            
            # Zero crossing rate - noisiness
            zcr = librosa.feature.zero_crossing_rate(y).mean()
            
            # Tempo
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            
            # Normalize values
            rms_norm = min(rms * 10, 1.0)  # Energy
            tempo_norm = min(tempo / 180.0, 1.0)  # Tempo
            zcr_norm = min(zcr * 100, 1.0)  # Noisiness
            
            # Enhanced scoring system with additional features
            scores = {
                'Anger': rms_norm * 0.6 + zcr_norm * 0.2 + spectral_features['spectral_contrast'] * 0.2,
                'Joy': rms_norm * 0.4 + tempo_norm * 0.3 + chroma.mean() * 0.3,
                'Sadness': (1 - rms_norm) * 0.5 + (1 - tempo_norm) * 0.3 + (1 - mel_mean) * 0.2,
                'Fear': zcr_norm * 0.4 + (1 - rms_norm) * 0.3 + spectral_features['spectral_rolloff'] * 0.3,
                'Surprise': zcr_norm * 0.5 + tempo_norm * 0.3 + mel_std * 0.2,
                'Disgust': (1 - zcr_norm) * 0.4 + spectral_features['spectral_centroid'] * 0.4 + (1 - chroma.std()) * 0.2,
                'Calm': (1 - zcr_norm) * 0.6 + (1 - rms_norm) * 0.2 + (1 - spectral_features['spectral_contrast']) * 0.2
            }
            
            # Get primary and secondary emotions
            sorted_emotions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            primary_emotion = sorted_emotions[0][0]
            secondary_emotion = sorted_emotions[1][0]
            
            # Calculate enhanced intensity
            intensity = self.calculate_enhanced_intensity(audio_path, spectral_features)
            
            return {
                'primary_emotion': primary_emotion,
                'secondary_emotion': secondary_emotion,
                'confidence': sorted_emotions[0][1],
                'secondary_confidence': sorted_emotions[1][1],
                'intensity': intensity,
                'duration': duration,
                'spectral_features': spectral_features
            }
        
        except Exception as e:
            print(f"Error in enhanced fallback emotion detection: {e}")
            return {
                'primary_emotion': 'Calm',
                'confidence': 0.5,
                'intensity': 0.5,
                'duration': duration
            }
    
    def calculate_enhanced_intensity(self, audio_path, spectral_features=None):
        """
        Calculate emotional intensity based on audio energy and spectral features
        """
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Calculate RMS energy
            rms = librosa.feature.rms(y=y).mean()
            
            # Calculate onset strength - related to the strength of onsets/beats
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            onset_mean = onset_env.mean()
            
            # Calculate dynamic range
            dynamic_range = np.abs(y).max() - np.abs(y).min()
            
            # Combine features for intensity calculation
            base_intensity = min(rms * 10, 1.0)
            onset_factor = min(onset_mean * 5, 1.0)
            dynamic_factor = min(dynamic_range * 2, 1.0)
            
            # If spectral features are available, use them to refine intensity
            if spectral_features:
                spectral_factor = (
                    spectral_features['spectral_contrast'] * 0.4 + 
                    spectral_features['spectral_centroid'] * 0.3 + 
                    spectral_features['spectral_rolloff'] * 0.3
                )
                
                # Weighted combination of all factors
                intensity = (
                    base_intensity * 0.4 + 
                    onset_factor * 0.3 + 
                    dynamic_factor * 0.1 + 
                    spectral_factor * 0.2
                )
            else:
                # Without spectral features
                intensity = base_intensity * 0.6 + onset_factor * 0.3 + dynamic_factor * 0.1
            
            return float(intensity)
        
        except Exception as e:
            print(f"Error calculating enhanced intensity: {e}")
            return 0.5