import os
import numpy as np
import pandas as pd
import librosa
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv1D, MaxPooling1D, BatchNormalization
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import glob
import tqdm

# Define paths
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'training')
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'emotion_model.h5')
TFLITE_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'emotion_model.tflite')

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
        
        # Pad or truncate to fixed length
        pad_width = max_pad_len - mfccs.shape[1]
        if pad_width > 0:
            mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
        else:
            mfccs = mfccs[:, :max_pad_len]
        
        return mfccs
    
    except Exception as e:
        print(f"Error extracting features from {file_path}: {e}")
        return None

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
            mfccs = extract_features(file_path)
            
            if mfccs is not None:
                features.append(mfccs)
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

def build_model(input_shape, num_classes):
    """
    Build CNN model for emotion classification
    """
    model = Sequential()
    
    # First convolutional layer
    model.add(Conv1D(64, 3, padding='same', activation='relu', input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.2))
    
    # Second convolutional layer
    model.add(Conv1D(128, 3, padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.2))
    
    # Third convolutional layer
    model.add(Conv1D(256, 3, padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.2))
    
    # Flatten and dense layers
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    
    # Output layer
    model.add(Dense(num_classes, activation='softmax'))
    
    # Compile model
    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )
    
    return model

def train_model():
    """
    Train emotion detection model
    """
    # Load data
    print("Loading and processing data...")
    features, labels = load_data(DATA_PATH)
    
    if features is None or labels is None:
        print("Failed to load data. Exiting.")
        return
    
    print(f"Loaded {len(features)} samples.")
    
    # Reshape features for CNN input
    features = features.reshape(features.shape[0], features.shape[1], features.shape[2], 1)
    
    # Convert labels to categorical
    labels = to_categorical(labels)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=42
    )
    
    # Build model
    print("Building model...")
    input_shape = (X_train.shape[1], X_train.shape[2])
    model = build_model(input_shape, len(emotions))
    
    # Print model summary
    model.summary()
    
    # Train model
    print("Training model...")
    history = model.fit(
        X_train, y_train,
        batch_size=32,
        epochs=50,
        validation_data=(X_test, y_test),
        verbose=1
    )
    
    # Evaluate model
    print("Evaluating model...")
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test accuracy: {test_accuracy:.4f}")
    
    # Save model
    print(f"Saving model to {MODEL_PATH}...")
    model.save(MODEL_PATH)
    
    # Convert to TensorFlow Lite
    print("Converting to TensorFlow Lite...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    
    # Save TFLite model
    with open(TFLITE_MODEL_PATH, 'wb') as f:
        f.write(tflite_model)
    
    print(f"TensorFlow Lite model saved to {TFLITE_MODEL_PATH}")
    
    # Plot training history
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(MODEL_PATH), 'training_history.png'))
    plt.close()

if __name__ == "__main__":
    train_model()