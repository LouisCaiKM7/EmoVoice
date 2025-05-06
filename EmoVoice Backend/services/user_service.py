import os
import uuid
import datetime
import hashlib
import secrets
import json

class UserService:
    def __init__(self, database_service):
        """
        Initialize the user service with a database service
        """
        self.db_service = database_service
    
    def register_user(self, name, email, password):
        """
        Register a new user
        """
        # Check if email is already registered
        # In a real implementation, you would query the database
        
        # Generate a unique user ID
        user_id = str(uuid.uuid4())
        
        # Generate password hash and salt
        salt = secrets.token_hex(16)
        password_hash = self._hash_password(password, salt)
        
        # Create user data
        user_data = {
            'id': user_id,
            'name': name,
            'email': email,
            'password_hash': f"{salt}:{password_hash}",
            'created_at': datetime.datetime.now().isoformat(),
            'preferences': {
                'theme': 'system',
                'notifications': True,
                'privacy': {
                    'store_recordings': True,
                    'analytics': True
                }
            }
        }
        
        # Save user to database
        self.db_service.save_user(user_data)
        
        # Return user data without password
        user_data.pop('password_hash')
        return user_data
    
    def authenticate_user(self, email, password):
        """
        Authenticate a user
        """
        # In a real implementation, you would:
        # 1. Look up the user by email
        # 2. Verify the password hash
        # 3. Return the user data if valid
        
        # For now, we'll just return a placeholder
        return {
            'status': 'error',
            'message': 'Authentication not implemented'
        }
    
    def update_user_preferences(self, user_id, preferences):
        """
        Update user preferences
        """
        # Get current user data
        user = self.db_service.get_user(user_id)
        
        if not user:
            return {
                'status': 'error',
                'message': 'User not found'
            }
        
        # Update preferences
        user['preferences'].update(preferences)
        
        # Save updated user data
        self.db_service.save_user(user)
        
        return {
            'status': 'success',
            'preferences': user['preferences']
        }
    
    def _hash_password(self, password, salt):
        """
        Hash a password with a salt using SHA-256
        """
        return hashlib.sha256((password + salt).encode()).hexdigest()