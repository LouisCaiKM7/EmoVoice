import os
import uuid
import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from collections import Counter
import numpy as np

class ReportService:
    def __init__(self, database_service):
        """
        Initialize the report service with a database service
        """
        self.db_service = database_service
        
        # Ensure reports directory exists
        self.reports_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data',
            'reports'
        )
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_emotion_report(self, user_id, time_range='week', title=None, description=None):
        """
        Generate an emotion report for a user
        """
        # Get emotions for the user within the time range
        emotions = self.db_service.get_emotions(user_id, time_range)
        
        if not emotions:
            return {
                'status': 'error',
                'message': 'No emotion data found for the specified time range'
            }
        
        # Get recordings for the user
        recordings = self.db_service.get_recordings(user_id)
        
        # Create a mapping of recording_id to recording data
        recording_map = {r['id']: r for r in recordings}
        
        # Process emotion data
        emotion_counts = Counter()
        emotion_intensities = {}
        emotion_confidences = {}
        emotion_timeline = []
        
        for emotion in emotions:
            primary_emotion = emotion['primary_emotion']
            recording_id = emotion['recording_id']
            
            # Count emotions
            emotion_counts[primary_emotion] += 1
            
            # Track intensities
            if primary_emotion not in emotion_intensities:
                emotion_intensities[primary_emotion] = []
            emotion_intensities[primary_emotion].append(emotion['intensity'])
            
            # Track confidences
            if primary_emotion not in emotion_confidences:
                emotion_confidences[primary_emotion] = []
            emotion_confidences[primary_emotion].append(emotion['primary_confidence'])
            
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
        
        # Calculate average intensities and confidences
        avg_intensities = {e: sum(vals)/len(vals) for e, vals in emotion_intensities.items()}
        avg_confidences = {e: sum(vals)/len(vals) for e, vals in emotion_confidences.items()}
        
        # Generate charts
        emotion_distribution_chart = self._generate_emotion_distribution_chart(emotion_counts)
        emotion_timeline_chart = self._generate_emotion_timeline_chart(emotion_timeline)
        emotion_intensity_chart = self._generate_emotion_intensity_chart(avg_intensities)
        
        # Generate insights
        insights = self._generate_insights(emotion_counts, avg_intensities, emotion_timeline)
        
        # Create report data
        report_data = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'title': title or f"Emotion Report - {datetime.datetime.now().strftime('%Y-%m-%d')}",
            'description': description or f"Emotion analysis for the past {time_range}",
            'time_range': time_range,
            'created_at': datetime.datetime.now().isoformat(),
            'data': {
                'emotion_counts': dict(emotion_counts),
                'avg_intensities': avg_intensities,
                'avg_confidences': avg_confidences,
                'emotion_timeline': emotion_timeline,
                'charts': {
                    'emotion_distribution': emotion_distribution_chart,
                    'emotion_timeline': emotion_timeline_chart,
                    'emotion_intensity': emotion_intensity_chart
                },
                'insights': insights
            }
        }
        
        # Save report to database
        self.db_service.save_report(report_data)
        
        return {
            'status': 'success',
            'report_id': report_data['id'],
            'report': report_data
        }
    
    def _generate_emotion_distribution_chart(self, emotion_counts):
        """
        Generate a pie chart of emotion distribution
        """
        try:
            plt.figure(figsize=(8, 6))
            labels = list(emotion_counts.keys())
            sizes = list(emotion_counts.values())
            
            # Define colors for emotions
            colors = {
                'Anger': '#FF5252',
                'Disgust': '#66BB6A',
                'Fear': '#7E57C2',
                'Joy': '#FFD700',
                'Sadness': '#4FC3F7',
                'Surprise': '#FF4081',
                'Calm': '#81D4FA'
            }
            
            # Get colors for the emotions in our data
            chart_colors = [colors.get(emotion, '#CCCCCC') for emotion in labels]
            
            plt.pie(sizes, labels=labels, colors=chart_colors, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.title('Emotion Distribution')
            
            # Save chart to BytesIO
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            
            # Convert to base64
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            
            return base64.b64encode(image_png).decode('utf-8')
        
        except Exception as e:
            print(f"Error generating emotion distribution chart: {e}")
            return None
    
    def _generate_emotion_timeline_chart(self, emotion_timeline):
        """
        Generate a timeline chart of emotions
        """
        try:
            if not emotion_timeline:
                return None
                
            # Convert to DataFrame
            df = pd.DataFrame(emotion_timeline)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Define colors for emotions
            colors = {
                'Anger': '#FF5252',
                'Disgust': '#66BB6A',
                'Fear': '#7E57C2',
                'Joy': '#FFD700',
                'Sadness': '#4FC3F7',
                'Surprise': '#FF4081',
                'Calm': '#81D4FA'
            }
            
            plt.figure(figsize=(10, 6))
            
            # Group by day and emotion, count occurrences
            df['date'] = df['timestamp'].dt.date
            emotion_counts = df.groupby(['date', 'emotion']).size().unstack().fillna(0)
            
            # Plot stacked bar chart
            emotion_counts.plot(kind='bar', stacked=True, ax=plt.gca(), color=[colors.get(e, '#CCCCCC') for e in emotion_counts.columns])
            
            plt.title('Emotion Timeline')
            plt.xlabel('Date')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save chart to BytesIO
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            
            # Convert to base64
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            
            return base64.b64encode(image_png).decode('utf-8')
        
        except Exception as e:
            print(f"Error generating emotion timeline chart: {e}")
            return None
    
    def _generate_emotion_intensity_chart(self, avg_intensities):
        """
        Generate a bar chart of average emotion intensities
        """
        try:
            plt.figure(figsize=(8, 6))
            
            # Define colors for emotions
            colors = {
                'Anger': '#FF5252',
                'Disgust': '#66BB6A',
                'Fear': '#7E57C2',
                'Joy': '#FFD700',
                'Sadness': '#4FC3F7',
                'Surprise': '#FF4081',
                'Calm': '#81D4FA'
            }
            
            emotions = list(avg_intensities.keys())
            intensities = list(avg_intensities.values())
            bar_colors = [colors.get(emotion, '#CCCCCC') for emotion in emotions]
            
            plt.bar(emotions, intensities, color=bar_colors)
            plt.title('Average Emotion Intensities')
            plt.xlabel('Emotion')
            plt.ylabel('Average Intensity')
            plt.ylim(0, 1)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save chart to BytesIO
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            
            # Convert to base64
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            
            return base64.b64encode(image_png).decode('utf-8')
        
        except Exception as e:
            print(f"Error generating emotion intensity chart: {e}")
            return None
    
    def _generate_insights(self, emotion_counts, avg_intensities, emotion_timeline):
        """
        Generate insights based on emotion data
        """
        insights = []
        
        # Get most common emotion
        if emotion_counts:
            most_common_emotion = emotion_counts.most_common(1)[0][0]
            insights.append({
                'type': 'most_common_emotion',
                'title': 'Most Common Emotion',
                'description': f"Your most frequently detected emotion was {most_common_emotion}."
            })
            
            # Add specific insights based on the most common emotion
            if most_common_emotion == 'Joy':
                insights.append({
                    'type': 'positive_insight',
                    'title': 'Positive Emotional State',
                    'description': "You've been experiencing a lot of joy lately. This positive emotional state can boost creativity and problem-solving abilities."
                })
            elif most_common_emotion == 'Sadness':
                insights.append({
                    'type': 'self_care',
                    'title': 'Self-Care Reminder',
                    'description': "You've been experiencing sadness frequently. Remember to practice self-care activities like gentle exercise, connecting with loved ones, or mindfulness."
                })
            elif most_common_emotion == 'Anger':
                insights.append({
                    'type': 'stress_management',
                    'title': 'Stress Management',
                    'description': "Your voice has been showing signs of anger. Consider stress-reduction techniques like deep breathing, meditation, or physical activity."
                })
            elif most_common_emotion == 'Fear':
                insights.append({
                    'type': 'anxiety_management',
                    'title': 'Anxiety Management',
                    'description': "Your voice patterns indicate fear or anxiety. Grounding exercises and mindfulness can help manage these feelings."
                })
        
        # Check for emotional variability
        if len(emotion_counts) >= 3:
            insights.append({
                'type': 'emotional_variability',
                'title': 'Emotional Variability',
                'description': "You've experienced a wide range of emotions, which is a sign of emotional flexibility and healthy emotional processing."
            })
        
        # Check for high intensity emotions
        high_intensity_emotions = [e for e, i in avg_intensities.items() if i > 0.7]
        if high_intensity_emotions:
            emotions_str = ', '.join(high_intensity_emotions)
            insights.append({
                'type': 'high_intensity',
                'title': 'High Emotional Intensity',
                'description': f"Your {emotions_str} emotions have been particularly intense. Strong emotions can provide valuable information about what matters to you."
            })
        
        # Check for emotional patterns over time
        if len(emotion_timeline) >= 5:
            # Simple pattern detection - look for consecutive same emotions
            consecutive_count = 1
            current_emotion = emotion_timeline[0]['emotion']
            max_consecutive = 1
            max_emotion = current_emotion
            
            for i in range(1, len(emotion_timeline)):
                if emotion_timeline[i]['emotion'] == current_emotion:
                    consecutive_count += 1
                    if consecutive_count > max_consecutive:
                        max_consecutive = consecutive_count
                        max_emotion = current_emotion
                else:
                    consecutive_count = 1
                    current_emotion = emotion_timeline[i]['emotion']
            
            if max_consecutive >= 3:
                insights.append({
                    'type': 'emotional_pattern',
                    'title': 'Emotional Pattern Detected',
                    'description': f"You've experienced {max_emotion} consistently across multiple recordings. Recognizing emotional patterns can help you understand your triggers and responses."
                })
        
        # Add general coping strategies
        coping_strategies = {
            'Anger': "Practice deep breathing or count to 10 before responding to triggering situations.",
            'Sadness': "Engage in activities that bring you joy, even small ones, and consider reaching out to supportive friends or family.",
            'Fear': "Try grounding techniques like the 5-4-3-2-1 method: acknowledge 5 things you see, 4 things you feel, 3 things you hear, 2 things you smell, and 1 thing you taste.",
            'Joy': "Savor these positive moments and consider journaling about them to revisit during challenging times.",
            'Surprise': "Use moments of surprise as opportunities for learning and growth.",
            'Disgust': "Practice acceptance and non-judgment of your emotional reactions.",
            'Calm': "Continue practices that promote this balanced state, such as regular meditation or mindfulness."
        }
        
        # Add coping strategy for the most common emotion
        if emotion_counts:
            most_common_emotion = emotion_counts.most_common(1)[0][0]
            if most_common_emotion in coping_strategies:
                insights.append({
                    'type': 'coping_strategy',
                    'title': f'Coping Strategy for {most_common_emotion}',
                    'description': coping_strategies[most_common_emotion]
                })
        
        return insights
    
    def share_report(self, report_id, recipient_email, expiration_days=7):
        """
        Share a report with someone via email
        """
        # Generate a unique access token
        access_token = str(uuid.uuid4())
        
        # Calculate expiration date
        expires_at = (datetime.datetime.now() + datetime.timedelta(days=expiration_days)).isoformat()
        
        # Create share data
        share_data = {
            'id': str(uuid.uuid4()),
            'report_id': report_id,
            'recipient_email': recipient_email,
            'access_token': access_token,
            'status': 'pending',
            'expires_at': expires_at
        }
        
        # Save share data to database
        self.db_service.save_report_share(share_data)
        
        # In a real application, you would send an email here
        # For now, we'll just return the access token
        
        return {
            'status': 'success',
            'share_id': share_data['id'],
            'access_token': access_token,
            'expires_at': expires_at
        }
    
    def get_report_by_token(self, access_token):
        """
        Get a report using an access token
        """
        # In a real implementation, you would:
        # 1. Look up the share by access token
        # 2. Check if it's expired
        # 3. Return the associated report if valid
        
        # For now, we'll just return a placeholder
        return {
            'status': 'error',
            'message': 'This feature is not yet implemented'
        }