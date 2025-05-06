import os
import json
import uuid
import datetime
import requests

class SmartHomeService:
    def __init__(self, database_service):
        """
        Initialize the smart home service with a database service
        """
        self.db_service = database_service
    
    def register_integration(self, user_id, provider, access_token=None, refresh_token=None, settings=None):
        """
        Register a new smart home integration
        """
        # Generate a unique integration ID
        integration_id = str(uuid.uuid4())
        
        # Create integration data
        integration_data = {
            'id': integration_id,
            'user_id': user_id,
            'provider': provider,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_expires_at': None,
            'settings': settings or {},
            'created_at': datetime.datetime.now().isoformat()
        }
        
        # Save integration to database
        self.db_service.save_smart_home_integration(integration_data)
        
        # Return integration data without sensitive tokens
        safe_data = integration_data.copy()
        safe_data.pop('access_token', None)
        safe_data.pop('refresh_token', None)
        return safe_data
    
    def get_integrations(self, user_id):
        """
        Get all smart home integrations for a user
        """
        integrations = self.db_service.get_smart_home_integrations(user_id)
        
        # Remove sensitive tokens
        for integration in integrations:
            integration.pop('access_token', None)
            integration.pop('refresh_token', None)
        
        return integrations
    
    def delete_integration(self, integration_id):
        """
        Delete a smart home integration
        """
        return self.db_service.delete_smart_home_integration(integration_id)
    
    def adjust_lighting(self, user_id, emotion, intensity):
        """
        Adjust smart home lighting based on detected emotion
        """
        # Get user's smart home integrations
        integrations = self.db_service.get_smart_home_integrations(user_id)
        
        results = []
        
        for integration in integrations:
            provider = integration['provider']
            
            # Skip if no access token
            if not integration.get('access_token'):
                continue
            
            # Determine lighting settings based on emotion and intensity
            settings = self._get_lighting_settings(emotion, intensity)
            
            # Apply settings to the appropriate provider
            if provider == 'philips_hue':
                result = self._adjust_philips_hue(integration, settings)
            elif provider == 'google_home':
                result = self._adjust_google_home(integration, settings)
            else:
                result = {
                    'status': 'error',
                    'message': f'Unsupported provider: {provider}'
                }
            
            results.append({
                'provider': provider,
                'result': result
            })
        
        return results
    
    def _get_lighting_settings(self, emotion, intensity):
        """
        Get lighting settings based on emotion and intensity
        """
        # Default settings
        settings = {
            'brightness': 100,  # 0-100
            'color': {
                'hue': 0,       # 0-360
                'saturation': 0 # 0-100
            }
        }
        
        # Adjust settings based on emotion
        if emotion == 'Joy':
            # Warm yellow
            settings['color']['hue'] = 45
            settings['color']['saturation'] = 80
            settings['brightness'] = min(100, 70 + (intensity * 30))
        elif emotion == 'Sadness':
            # Soft blue
            settings['color']['hue'] = 240
            settings['color']['saturation'] = 40
            settings['brightness'] = max(30, 60 - (intensity * 30))
        elif emotion == 'Anger':
            # Soft red
            settings['color']['hue'] = 0
            settings['color']['saturation'] = 60
            settings['brightness'] = min(100, 60 + (intensity * 40))
        elif emotion == 'Fear':
            # Purple
            settings['color']['hue'] = 270
            settings['color']['saturation'] = 50
            settings['brightness'] = max(30, 70 - (intensity * 40))
        elif emotion == 'Surprise':
            # Bright cyan
            settings['color']['hue'] = 180
            settings['color']['saturation'] = 70
            settings['brightness'] = min(100, 70 + (intensity * 30))
        elif emotion == 'Disgust':
            # Green
            settings['color']['hue'] = 120
            settings['color']['saturation'] = 50
            settings['brightness'] = max(40, 70 - (intensity * 30))
        elif emotion == 'Calm':
            # Soft white
            settings['color']['hue'] = 30
            settings['color']['saturation'] = 20
            settings['brightness'] = 60
        
        return settings
    
    def _adjust_philips_hue(self, integration, settings):
        """
        Adjust Philips Hue lights
        """
        # In a real implementation, you would:
        # 1. Use the Philips Hue API to adjust lights
        # 2. Handle authentication and token refresh
        # 3. Return success or error
        
        # For now, we'll just return a placeholder
        return {
            'status': 'success',
            'message': 'Lighting adjusted (simulated)',
            'settings': settings
        }
    
    def _adjust_google_home(self, integration, settings):
        """
        Adjust Google Home lights
        """
        # In a real implementation, you would:
        # 1. Use the Google Home API to adjust lights
        # 2. Handle authentication and token refresh
        # 3. Return success or error
        
        # For now, we'll just return a placeholder
        return {
            'status': 'success',
            'message': 'Lighting adjusted (simulated)',
            'settings': settings
        }