import os
import uuid
import datetime
import wave
import numpy as np
import soundfile as sf

class RecordingService:
    def __init__(self, database_service, emotion_detection_service):
        """
        Initialize the recording service with database and emotion detection services
        """
        self.db_service = database_service
        self.emotion_service = emotion_detection_service
        
        # Ensure recordings directory exists
        self.recordings_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data',
            'recordings'
        )
        os.makedirs(self.recordings_dir, exist_ok=True)
    
    def save_recording(self, user_id, audio_data, filename=None):
        """
        Save a recording and analyze emotions
        """
        # Generate a unique recording ID
        recording_id = str(uuid.uuid4())
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{user_id}_{timestamp}.wav"
        
        # Create file path
        file_path = os.path.join(self.recordings_dir, filename)
        
        # Save audio data to file
        try:
            # Assuming audio_data is a bytes object
            with open(file_path, 'wb') as f:
                f.write(audio_data)
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Get audio duration
            with wave.open(file_path, 'rb') as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                duration = frames / float(rate)
            
            # Create recording data
            recording_data = {
                'id': recording_id,
                'user_id': user_id,
                'filename': filename,
                'file_path': file_path,
                'file_size': file_size,
                'duration': duration,
                'created_at': datetime.datetime.now().isoformat()
            }
            
            # Save recording to database
            self.db_service.save_recording(recording_data)
            
            # Analyze emotions
            emotion_result = self.emotion_service.analyze_audio(file_path)
            
            # Add recording ID to emotion data
            emotion_data = {
                'id': str(uuid.uuid4()),
                'recording_id': recording_id,
                'primary_emotion': emotion_result['primary_emotion'],
                'secondary_emotion': emotion_result.get('secondary_emotion'),
                'primary_confidence': emotion_result.get('confidence', 0),
                'secondary_confidence': emotion_result.get('secondary_confidence', 0),
                'intensity': emotion_result.get('intensity', 0),
                'created_at': datetime.datetime.now().isoformat()
            }
            
            # Save emotion data to database
            self.db_service.save_emotion(emotion_data)
            
            return {
                'status': 'success',
                'recording_id': recording_id,
                'emotion': emotion_data
            }
        
        except Exception as e:
            print(f"Error saving recording: {e}")
            # Clean up file if it was created
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_recording(self, recording_id):
        """
        Get a recording by ID
        """
        # In a real implementation, you would query the database
        # For now, we'll just return a placeholder
        return {
            'status': 'error',
            'message': 'This feature is not yet implemented'
        }
    
    def delete_recording(self, recording_id, user_id):
        """
        Delete a recording
        """
        # In a real implementation, you would:
        # 1. Check if the recording belongs to the user
        # 2. Delete the file
        # 3. Delete the database record
        
        # For now, we'll just return a placeholder
        return {
            'status': 'error',
            'message': 'This feature is not yet implemented'
        }