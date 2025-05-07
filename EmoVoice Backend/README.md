# EmoVoice Backend

EmoVoice is an AI-powered emotion detection system that analyzes voice to detect emotions and provide insights.

## Features

- Real-time voice emotion analysis (anger, joy, sadness, etc.)
- Mood timeline tracking with actionable insights
- Anonymous sharing of emotional reports with therapists
- Smart home integration (adjust lighting based on mood)
- On-device processing for privacy

## Project Structure
EmoVoice Backend/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── train_model.py              # Script to train emotion detection model
├── data/                       # Data directory
│   ├── recordings/             # User recordings
│   ├── reports/                # Generated reports
│   ├── training/               # Training data for model
│   └── emovoice.db             # SQLite database
├── database/                   # Database files
│   └── schema.sql              # Database schema
├── models/                     # Model files
│   └── emotion_model.tflite    # TensorFlow Lite model
└── services/                   # Service modules
├── database_service.py     # Database operations
├── emotion_detection_service.py # Emotion detection
├── insight_service.py      # Insight generation
├── recording_service.py    # Recording management
├── report_service.py       # Report generation
├── smart_home_service.py   # Smart home integration
└── user_service.py         # User managemen


## Setup and Installation

1. Clone the repository

2. Install dependencies:
``` bash
pip install -r requirements.txt
```

3. Initialize the database:
``` bash
python -c "from services.database_service import DatabaseService; DatabaseService('data/emovoice.db').init_database()"
```
4. Train the emotion detection model (optional, pre-trained model included):
``` bash
python train_model.py
```
5. Run the Flask application:
``` bash
python app.py
```

## API Endpoints

### Health Check
- `GET /api/health` - Check if the API is running

### User Management
- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - Login a user
- `PUT /api/users/<user_id>/preferences` - Update user preferences

### Recording
- `POST /api/recordings` - Upload a new recording
- `GET /api/recordings/<user_id>` - Get recordings for a user
- `GET /api/recordings/<recording_id>/emotion` - Get emotion for a recording

### Reports
- `POST /api/reports` - Generate a new report
- `GET /api/reports/<user_id>` - Get reports for a user
- `POST /api/reports/<report_id>/share` - Share a report
- `GET /api/reports/shared/<token>` - Access a shared report

### Insights
- `GET /api/insights/<user_id>` - Get insights for a user
- `PUT /api/insights/<insight_id>/read` - Mark an insight as read

### Smart Home
- `POST /api/smart-home/integrate` - Register a smart home integration
- `GET /api/smart-home/<user_id>` - Get integrations for a user
- `DELETE /api/smart-home/<integration_id>` - Delete an integration
- `POST /api/smart-home/<user_id>/adjust` - Adjust lighting based on emotion

## Emotion Detection

The emotion detection system uses a Convolutional Neural Network (CNN) trained on MFCC features extracted from audio recordings. The model can detect the following emotions:

- Anger
- Disgust
- Fear
- Joy
- Sadness
- Surprise
- Calm

## Database Schema

The application uses SQLite for data storage with the following tables:

- `users` - User information
- `recordings` - Audio recordings
- `emotions` - Detected emotions
- `reports` - Generated reports
- `report_shares` - Shared reports
- `insights` - Generated insights
- `smart_home_integrations` - Smart home device integrations
