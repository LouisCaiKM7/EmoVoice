import sqlite3
import json
import os

class DatabaseService:
    def __init__(self, db_path):
        self.db_path = db_path
        # Ensure database directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    def get_connection(self):
        """Get a database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with schema"""
        try:
            # Read schema file
            schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                      'database', 'schema.sql')
            
            with open(schema_path, 'r') as f:
                schema = f.read()
            
            # Execute schema
            conn = self.get_connection()
            conn.executescript(schema)
            conn.commit()
            conn.close()
            
            print("Database initialized successfully")
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise
    
    # User operations
    def save_user(self, user_data):
        """Save user to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO users 
                (id, name, email, password_hash, created_at, preferences)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_data['id'],
                user_data['name'],
                user_data.get('email'),
                user_data.get('password_hash'),
                user_data.get('created_at', None),
                json.dumps(user_data.get('preferences', {}))
            ))
            
            conn.commit()
            return user_data['id']
        finally:
            conn.close()
    
    def get_user(self, user_id):
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            user = dict(row)
            # Parse JSON fields
            if user.get('preferences'):
                user['preferences'] = json.loads(user['preferences'])
            
            return user
        finally:
            conn.close()
    
    # Recording operations
    def save_recording(self, recording_data):
        """Save recording to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO recordings 
                (id, user_id, filename, duration, file_path, file_size)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                recording_data['id'],
                recording_data['user_id'],
                recording_data['filename'],
                recording_data.get('duration', 0),
                recording_data.get('file_path'),
                recording_data.get('file_size', 0)
            ))
            
            conn.commit()
            return recording_data['id']
        finally:
            conn.close()
    
    def get_recordings(self, user_id, limit=50):
        """Get recordings for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM recordings 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (user_id, limit))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    # Emotion operations
    def save_emotion(self, emotion_data):
        """Save emotion data to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO emotions 
                (id, recording_id, primary_emotion, secondary_emotion, 
                primary_confidence, secondary_confidence, intensity)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                emotion_data['id'],
                emotion_data['recording_id'],
                emotion_data['primary_emotion'],
                emotion_data.get('secondary_emotion'),
                emotion_data.get('primary_confidence', 0),
                emotion_data.get('secondary_confidence', 0),
                emotion_data.get('intensity', 0)
            ))
            
            conn.commit()
            return emotion_data['id']
        finally:
            conn.close()
    
    def get_emotions(self, user_id, time_range='week'):
        """Get emotions for a user within a time range"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Calculate date range
            if time_range == 'week':
                date_filter = "datetime('now', '-7 days')"
            elif time_range == 'month':
                date_filter = "datetime('now', '-30 days')"
            else:
                date_filter = "datetime('now', '-365 days')"  # Default to a year
            
            cursor.execute(f'''
                SELECT e.* FROM emotions e
                JOIN recordings r ON e.recording_id = r.id
                WHERE r.user_id = ? AND r.created_at >= {date_filter}
                ORDER BY r.created_at DESC
            ''', (user_id,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    # Report operations
    def save_report(self, report_data):
        """Save report to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO reports 
                (id, user_id, title, description, time_range, 
                start_date, end_date, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                report_data['id'],
                report_data['user_id'],
                report_data.get('title'),
                report_data.get('description'),
                report_data['time_range'],
                report_data.get('start_date'),
                report_data.get('end_date'),
                json.dumps(report_data.get('data', {}))
            ))
            
            conn.commit()
            return report_data['id']
        finally:
            conn.close()
    
    def save_report_share(self, share_data):
        """Save report share to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO report_shares 
                (id, report_id, recipient_email, access_token, status, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                share_data['id'],
                share_data['report_id'],
                share_data['recipient_email'],
                share_data['access_token'],
                share_data.get('status', 'pending'),
                share_data.get('expires_at')
            ))
            
            conn.commit()
            return share_data['id']
        finally:
            conn.close()