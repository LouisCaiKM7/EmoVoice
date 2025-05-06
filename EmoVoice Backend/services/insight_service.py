import os
import uuid
import datetime
import json
from collections import Counter

class InsightService:
    def __init__(self, database_service):
        """
        Initialize the insight service with a database service
        """
        self.db_service = database_service
    
    def generate_insights(self, user_id):
        """
        Generate insights for a user based on their emotion data
        """
        # Get emotions for the user
        emotions = self.db_service.get_emotions(user_id, time_range='month')
        
        if not emotions:
            return {
                'status': 'error',
                'message': 'No emotion data found'
            }
        
        # Get recordings for the user
        recordings = self.db_service.get_recordings(user_id)
        
        # Create a mapping of recording_id to recording data
        recording_map = {r['id']: r for r in recordings}
        
        # Process emotion data
        emotion_counts = Counter()
        emotion_timeline = []
        
        for emotion in emotions:
            primary_emotion = emotion['primary_emotion']
            recording_id = emotion['recording_id']
            
            # Count emotions
            emotion_counts[primary_emotion] += 1
            
            # Add to timeline if we have the recording
            if recording_id in recording_map:
                recording = recording_map[recording_id]
                emotion_timeline.append({
                    'timestamp': recording['created_at'],
                    'emotion': primary_emotion,
                    'intensity': emotion['intensity'],
                    'confidence': emotion['primary_confidence'],
                    'recording_id': recording_id
                })
        
        # Sort timeline by timestamp
        emotion_timeline.sort(key=lambda x: x['timestamp'])
        
        # Generate insights
        insights = []
        
        # Dominant emotion insight
        if emotion_counts:
            dominant_emotion = emotion_counts.most_common(1)[0][0]
            insights.append(self._create_insight(
                user_id,
                f"Your dominant emotion is {dominant_emotion}",
                f"Over the past month, you've experienced {dominant_emotion} more than any other emotion. " +
                self._get_emotion_tip(dominant_emotion),
                'pattern'
            ))
        
        # Emotion pattern insights
        if len(emotion_timeline) >= 3:
            # Check for repeated patterns
            for i in range(len(emotion_timeline) - 2):
                if (emotion_timeline[i]['emotion'] == emotion_timeline[i+2]['emotion'] and
                    emotion_timeline[i]['emotion'] != emotion_timeline[i+1]['emotion']):
                    pattern_emotion = emotion_timeline[i]['emotion']
                    trigger_emotion = emotion_timeline[i+1]['emotion']
                    insights.append(self._create_insight(
                        user_id,
                        f"{trigger_emotion} often leads back to {pattern_emotion}",
                        f"We've noticed that when you experience {trigger_emotion}, you often return to {pattern_emotion} afterward. " +
                        f"This could indicate a recurring emotional pattern worth exploring.",
                        'pattern'
                    ))
                    break
        
        # Time-based insights
        if len(emotion_timeline) >= 5:
            # Convert timestamps to datetime objects
            for entry in emotion_timeline:
                entry['datetime'] = datetime.datetime.fromisoformat(entry['timestamp'])
            
            # Group by hour of day
            hour_emotions = {}
            for entry in emotion_timeline:
                hour = entry['datetime'].hour
                if hour not in hour_emotions:
                    hour_emotions[hour] = []
                hour_emotions[hour].append(entry['emotion'])
            
            # Find dominant emotions by time of day
            for period, hours in [('morning', range(5, 12)), ('afternoon', range(12, 18)), 
                                 ('evening', range(18, 22)), ('night', range(22, 24))]:
                period_emotions = []
                for hour in hours:
                    if hour in hour_emotions:
                        period_emotions.extend(hour_emotions[hour])
                
                if period_emotions:
                    period_counter = Counter(period_emotions)
                    dominant = period_counter.most_common(1)[0][0]
                    
                    insights.append(self._create_insight(
                        user_id,
                        f"You tend to feel {dominant} in the {period}",
                        f"Based on your emotional patterns, you most often experience {dominant} during the {period}. " +
                        self._get_time_tip(period, dominant),
                        'pattern'
                    ))
        
        # Save insights to database
        for insight in insights:
            self.db_service.save_insight(insight)
        
        return {
            'status': 'success',
            'insights': insights
        }
    
    def get_insights(self, user_id, unread_only=False):
        """
        Get insights for a user
        """
        insights = self.db_service.get_insights(user_id, unread_only)
        return insights
    
    def mark_insight_read(self, insight_id):
        """
        Mark an insight as read
        """
        return self.db_service.update_insight(insight_id, {'is_read': True})
    
    def _create_insight(self, user_id, title, description, category):
        """
        Create a new insight
        """
        return {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'title': title,
            'description': description,
            'category': category,
            'created_at': datetime.datetime.now().isoformat(),
            'is_read': False
        }
    
    def _get_emotion_tip(self, emotion):
        """
        Get a tip based on an emotion
        """
        tips = {
            'Joy': "Embrace this positive emotion and try to identify what triggers it so you can recreate these moments.",
            'Sadness': "Remember that sadness is a natural emotion. Consider journaling or talking with someone you trust.",
            'Anger': "When you feel anger rising, try deep breathing exercises or stepping away from the situation temporarily.",
            'Fear': "Grounding techniques like the 5-4-3-2-1 method can help manage fear and anxiety.",
            'Surprise': "Unexpected events can be opportunities for growth. Reflect on what surprised you and why.",
            'Disgust': "This emotion often signals a violation of your values. Reflect on what triggered this feeling.",
            'Calm': "Notice what brings you to this balanced state and try to incorporate more of these elements into your routine."
        }
        
        return tips.get(emotion, "Reflect on what triggers this emotion and how it affects you.")
    
    def _get_time_tip(self, period, emotion):
        """
        Get a tip based on time of day and emotion
        """
        if period == 'morning' and emotion in ['Sadness', 'Anger', 'Fear']:
            return "Starting your day with these emotions can affect your whole day. Consider a morning routine with mindfulness or exercise."
        elif period == 'afternoon' and emotion in ['Sadness', 'Anger', 'Fear']:
            return "Afternoon slumps are common. A short walk or brief meditation might help shift your emotional state."
        elif period == 'evening' and emotion in ['Sadness', 'Anger', 'Fear']:
            return "Evening emotions can affect sleep. Try a calming activity before bed like reading or gentle stretching."
        elif period == 'night' and emotion in ['Sadness', 'Anger', 'Fear']:
            return "Nighttime emotions can disrupt sleep. Consider a digital sunset an hour before bed and a relaxing bedtime routine."
        else:
            return "Being aware of your emotional patterns at different times of day can help you prepare and respond effectively."