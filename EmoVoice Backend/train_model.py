import os
import numpy as np
import pandas as pd
import librosa
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import glob
import tqdm

# Define paths
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'training')
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'emotion_model.joblib')

# Ensure directories exist
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

# Define emotions to detect
emotions = ['Anger', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Calm']

def extract_features(file_path, max_pad_len=174):
    """
    Extract MFCC features from audio file
    """
    try:
        # Load audio file
        y, sr = librosa.load(file_path, sr=22050)
        
        # Trim silence
        y, _ = librosa.effects.trim(y, top_db=25)
        
        # Extract MFCCs
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        
        # Extract additional features
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        
        # Normalize features
        mfccs = normalize_features(mfccs)
        
        # Pad or truncate to fixed length
        pad_width = max_pad_len - mfccs.shape[1]
        if pad_width > 0:
            mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
        else:
            mfccs = mfccs[:, :max_pad_len]
        
        # Flatten the MFCCs
        mfccs_flattened = mfccs.flatten()
        
        # Add additional features
        additional_features = np.array([
            spectral_centroid.mean(),
            spectral_contrast.mean(),
            spectral_rolloff.mean()
        ])
        
        # Combine all features
        combined_features = np.concatenate((mfccs_flattened, additional_features))
        
        return combined_features
    
    except Exception as e:
        print(f"Error extracting features from {file_path}: {e}")
        return None

def normalize_features(features):
    """
    Normalize features to zero mean and unit variance
    """
    mean = features.mean(axis=1, keepdims=True)
    std = features.std(axis=1, keepdims=True) + 1e-10  # Avoid division by zero
    return (features - mean) / std

def load_data(data_path):
    """
    Load audio data and extract features
    """
    features = []
    labels = []
    
    # Check if data path exists
    if not os.path.exists(data_path):
        print(f"Data path {data_path} does not exist. Please download and prepare the dataset.")
        return None, None
    
    # Process each emotion folder
    for emotion in emotions:
        emotion_path = os.path.join(data_path, emotion)
        
        # Skip if folder doesn't exist
        if not os.path.exists(emotion_path):
            print(f"Emotion folder {emotion_path} does not exist. Skipping.")
            continue
        
        # Get all audio files
        files = glob.glob(os.path.join(emotion_path, "*.wav"))
        
        print(f"Processing {len(files)} files for emotion: {emotion}")
        
        # Process each file
        for file_path in tqdm.tqdm(files):
            extracted_features = extract_features(file_path)
            
            if extracted_features is not None:
                features.append(extracted_features)
                labels.append(emotion)
    
    # Convert to numpy arrays
    features = np.array(features)
    
    # Encode labels
    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(labels)
    
    # Save label encoder mapping
    label_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
    print("Label mapping:", label_mapping)
    
    return features, labels

def train_model():
    """
    Train a Random Forest model for emotion classification
    """
    print("Loading data...")
    features, labels = load_data(DATA_PATH)
    
    if features is None or labels is None:
        print("Failed to load data. Exiting.")
        return
    
    print(f"Data loaded: {features.shape[0]} samples")
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=42
    )
    
    print("Training Random Forest model...")
    
    # Create and train the model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=None,
        min_samples_split=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    print("\nModel evaluation:")
    print(classification_report(y_test, y_pred, target_names=emotions))
    
    # Save the model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    
    # Feature importance
    feature_importance = model.feature_importances_
    
    # Plot feature importance
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(feature_importance)), feature_importance)
    plt.title('Feature Importance')
    plt.xlabel('Feature Index')
    plt.ylabel('Importance')
    plt.tight_layout()
    
    # Save the plot
    plot_path = os.path.join(os.path.dirname(MODEL_PATH), 'feature_importance.png')
    plt.savefig(plot_path)
    print(f"Feature importance plot saved to {plot_path}")

if __name__ == "__main__":
    train_model()