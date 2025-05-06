import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import uuid
import datetime
import json

# Import services
from services.database_service import DatabaseService
from services.emotion_detection_service import EmotionDetectionService
from services.recording_service import RecordingService
from services.report_service import ReportService
from services.user_service import UserService
from services.insight_service import InsightService
from services.smart_home_service import SmartHomeService

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize services
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'emovoice.db')
db_service = DatabaseService(db_path)
emotion_service = EmotionDetectionService()
recording_service = RecordingService(db_service, emotion_service)
report_service = ReportService(db_service)
user_service = UserService(db_service)
insight_service = InsightService(db_service)
smart_home_service = SmartHomeService(db_service)

# Ensure database is initialized
try:
    db_service.init_database()
except Exception as e:
    print(f"Error initializing database: {e}")

# Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.datetime.now().isoformat()
    })

# User routes
@app.route('/api/users/register', methods=['POST'])
def register_user():
    """Register a new user"""
    data = request.json
    
    if not data or not all(k in data for k in ['name', 'email', 'password']):
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields'
        }), 400
    
    result = user_service.register_user(
        data['name'],
        data['email'],
        data['password']
    )
    
    return jsonify(result)

@app.route('/api/users/login', methods=['POST'])
def login_user():
    """Login a user"""
    data = request.json
    
    if not data or not all(k in data for k in ['email', 'password']):
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields'
        }), 400
    
    result = user_service.authenticate_user(
        data['email'],
        data['password']
    )
    
    return jsonify(result)

@app.route('/api/users/<user_id>/preferences', methods=['PUT'])
def update_preferences(user_id):
    """Update user preferences"""
    data = request.json
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No preference data provided'
        }), 400
    
    result = user_service.update_user_preferences(user_id, data)
    return jsonify(result)

# Recording routes
@app.route('/api/recordings', methods=['POST'])
def upload_recording():
    """Upload a new recording"""
    if 'audio' not in request.files:
        return jsonify({
            'status': 'error',
            'message': 'No audio file provided'
        }), 400
    
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({
            'status': 'error',
            'message': 'User ID is required'
        }), 400
    
    audio_file = request.files['audio']
    audio_data = audio_file.read()
    
    result = recording_service.save_recording(user_id, audio_data, audio_file.filename)
    
    # Generate insights based on the new recording
    if result.get('status') == 'success' and 'recording_id' in result:
        insight_service.generate_insights_from_recording(user_id, result['recording_id'])
        
        # Update smart home devices based on detected emotion
        if 'emotion' in result:
            smart_home_service.adjust_devices_for_emotion(user_id, result['emotion'])
    
    return jsonify(result)

@app.route('/api/users/<user_id>/recordings', methods=['GET'])
def get_user_recordings(user_id):
    """Get recordings for a user"""
    limit = request.args.get('limit', 50, type=int)
    
    recordings = db_service.get_recordings(user_id, limit)
    
    return jsonify({
        'status': 'success',
        'recordings': recordings
    })

@app.route('/api/recordings/<recording_id>', methods=['GET'])
def get_recording(recording_id):
    """Get a specific recording"""
    recording = db_service.get_recording_by_id(recording_id)
    
    if not recording:
        return jsonify({
            'status': 'error',
            'message': 'Recording not found'
        }), 404
    
    return jsonify({
        'status': 'success',
        'recording': recording
    })

@app.route('/api/recordings/<recording_id>/audio', methods=['GET'])
def get_recording_audio(recording_id):
    """Get the audio file for a recording"""
    recording = db_service.get_recording_by_id(recording_id)
    
    if not recording or 'file_path' not in recording:
        return jsonify({
            'status': 'error',
            'message': 'Recording audio not found'
        }), 404
    
    return send_file(recording['file_path'], mimetype='audio/wav')

# Emotion routes
@app.route('/api/users/<user_id>/emotions', methods=['GET'])
def get_user_emotions(user_id):
    """Get emotions for a user"""
    time_range = request.args.get('time_range', 'week')
    
    emotions = db_service.get_emotions(user_id, time_range)
    
    return jsonify({
        'status': 'success',
        'emotions': emotions
    })

@app.route('/api/emotions/analyze', methods=['POST'])
def analyze_emotion():
    """Analyze emotion from audio without saving"""
    if 'audio' not in request.files:
        return jsonify({
            'status': 'error',
            'message': 'No audio file provided'
        }), 400
    
    audio_file = request.files['audio']
    audio_data = audio_file.read()
    
    result = emotion_service.detect_emotion(audio_data)
    
    return jsonify({
        'status': 'success',
        'emotion': result
    })

# Report routes
@app.route('/api/reports', methods=['POST'])
def create_report():
    """Create a new report"""
    data = request.json
    
    if not data or 'user_id' not in data:
        return jsonify({
            'status': 'error',
            'message': 'User ID is required'
        }), 400
    
    result = report_service.generate_emotion_report(
        data['user_id'],
        data.get('time_range', 'week'),
        data.get('title'),
        data.get('description')
    )
    
    return jsonify(result)

@app.route('/api/users/<user_id>/reports', methods=['GET'])
def get_user_reports(user_id):
    """Get reports for a user"""
    reports = db_service.get_reports(user_id)
    
    return jsonify({
        'status': 'success',
        'reports': reports
    })

@app.route('/api/reports/<report_id>', methods=['GET'])
def get_report(report_id):
    """Get a specific report"""
    report = db_service.get_report_by_id(report_id)
    
    if not report:
        return jsonify({
            'status': 'error',
            'message': 'Report not found'
        }), 404
    
    return jsonify({
        'status': 'success',
        'report': report
    })

@app.route('/api/reports/<report_id>/share', methods=['POST'])
def share_report(report_id):
    """Share a report"""
    data = request.json
    
    if not data or 'recipient_email' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Recipient email is required'
        }), 400
    
    result = report_service.share_report(
        report_id,
        data['recipient_email'],
        data.get('expiration_days', 7)
    )
    
    return jsonify(result)

@app.route('/api/shared-reports/<access_token>', methods=['GET'])
def get_shared_report(access_token):
    """Get a shared report using an access token"""
    result = report_service.get_report_by_token(access_token)
    
    return jsonify(result)

# Insight routes
@app.route('/api/users/<user_id>/insights', methods=['GET'])
def get_user_insights(user_id):
    """Get insights for a user"""
    category = request.args.get('category')
    limit = request.args.get('limit', 10, type=int)
    
    insights = insight_service.get_insights(user_id, category, limit)
    
    return jsonify({
        'status': 'success',
        'insights': insights
    })

@app.route('/api/insights/<insight_id>/read', methods=['POST'])
def mark_insight_read(insight_id):
    """Mark an insight as read"""
    result = insight_service.mark_insight_read(insight_id)
    
    return jsonify(result)

@app.route('/api/users/<user_id>/insights/generate', methods=['POST'])
def generate_user_insights(user_id):
    """Generate new insights for a user"""
    result = insight_service.generate_insights(user_id)
    
    return jsonify(result)

# Smart home integration routes
@app.route('/api/users/<user_id>/smart-home/integrations', methods=['GET'])
def get_smart_home_integrations(user_id):
    """Get smart home integrations for a user"""
    integrations = smart_home_service.get_integrations(user_id)
    
    return jsonify({
        'status': 'success',
        'integrations': integrations
    })

@app.route('/api/users/<user_id>/smart-home/integrations', methods=['POST'])
def add_smart_home_integration(user_id):
    """Add a new smart home integration"""
    data = request.json
    
    if not data or not all(k in data for k in ['provider', 'access_token']):
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields'
        }), 400
    
    result = smart_home_service.add_integration(
        user_id,
        data['provider'],
        data['access_token'],
        data.get('refresh_token'),
        data.get('settings', {})
    )
    
    return jsonify(result)

@app.route('/api/users/<user_id>/smart-home/integrations/<integration_id>', methods=['PUT'])
def update_smart_home_integration(user_id, integration_id):
    """Update a smart home integration"""
    data = request.json
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No update data provided'
        }), 400
    
    result = smart_home_service.update_integration(
        integration_id,
        data.get('access_token'),
        data.get('refresh_token'),
        data.get('settings')
    )
    
    return jsonify(result)

@app.route('/api/users/<user_id>/smart-home/integrations/<integration_id>', methods=['DELETE'])
def delete_smart_home_integration(user_id, integration_id):
    """Delete a smart home integration"""
    result = smart_home_service.delete_integration(integration_id)
    
    return jsonify(result)

@app.route('/api/users/<user_id>/smart-home/test', methods=['POST'])
def test_smart_home_integration(user_id):
    """Test smart home integration by sending a test command"""
    data = request.json
    
    if not data or 'integration_id' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Integration ID is required'
        }), 400
    
    result = smart_home_service.test_integration(
        data['integration_id'],
        data.get('command', 'test')
    )
    
    return jsonify(result)

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)