import * as SQLite from 'expo-sqlite';
import { Recording, Mood, Report } from '../types';

class DatabaseService {
  private db: SQLite.SQLiteDatabase;
  
  constructor() {
    try {
      this.db = SQLite.openDatabaseSync('emovoice.db');
      this.initDatabase();
    } catch (error) {
      console.error('Failed to open database:', error);
      throw new Error('Database initialization failed');
    }
  }
  
  private async initDatabase() {
    try {
      // Create tables if they don't exist
      await this.db.withTransactionAsync(async () => {
        // Recordings table
        await this.db.execAsync(
          `CREATE TABLE IF NOT EXISTS recordings (
            id TEXT PRIMARY KEY,
            date TEXT,
            duration TEXT,
            emotion TEXT,
            intensity REAL,
            audioUri TEXT
          )`
        );
        
        // Moods table
        await this.db.execAsync(
          `CREATE TABLE IF NOT EXISTS moods (
            id TEXT PRIMARY KEY,
            primary_emotion TEXT,
            secondary_emotion TEXT,
            intensity REAL,
            timestamp TEXT
          )`
        );
        
        // Reports table
        await this.db.execAsync(
          `CREATE TABLE IF NOT EXISTS reports (
            id TEXT PRIMARY KEY,
            date TEXT,
            recipient TEXT,
            status TEXT,
            time_range TEXT,
            data TEXT
          )`
        );
      });
    } catch (error) {
      console.error('Failed to initialize database tables:', error);
      throw new Error('Database table creation failed');
    }
  }
  
  // Recordings CRUD operations
  async saveRecording(recording: Recording): Promise<void> {
    try {
      await this.db.withTransactionAsync(async () => {
        await this.db.execAsync(
          `INSERT OR REPLACE INTO recordings (id, date, duration, emotion, intensity, audioUri)
           VALUES ('${this.escapeString(recording.id)}', '${this.escapeString(recording.date)}', 
                  '${this.escapeString(recording.duration)}', '${this.escapeString(recording.emotion)}', 
                  ${recording.intensity}, '${this.escapeString(recording.audioUri || '')}')`
        );
      });
    } catch (error) {
      console.error('Failed to save recording:', error);
      throw new Error('Could not save recording');
    }
  }
  
  async getRecordings(): Promise<Recording[]> {
    try {
      const result = await this.db.getAllAsync<Recording>('SELECT * FROM recordings ORDER BY date DESC');
      return result || [];
    } catch (error) {
      console.error('Failed to get recordings:', error);
      return [];
    }
  }
  
  // Mood CRUD operations
  async saveMood(mood: Mood): Promise<void> {
    try {
      const id = Date.now().toString();
      await this.db.withTransactionAsync(async () => {
        await this.db.execAsync(
          `INSERT INTO moods (id, primary_emotion, secondary_emotion, intensity, timestamp)
           VALUES ('${this.escapeString(id)}', '${this.escapeString(mood.primary)}', 
                  '${this.escapeString(mood.secondary || '')}', ${mood.intensity}, 
                  '${this.escapeString(mood.timestamp.toISOString())}')`
        );
      });
    } catch (error) {
      console.error('Failed to save mood:', error);
      throw new Error('Could not save mood data');
    }
  }
  
  async getMoods(limit: number = 10): Promise<Mood[]> {
    try {
      const rawResults = await this.db.getAllAsync<{
        id: string;
        primary_emotion: string;
        secondary_emotion: string;
        intensity: number;
        timestamp: string;
      }>(`SELECT * FROM moods ORDER BY timestamp DESC LIMIT ${limit}`);
      
      return (rawResults || []).map(item => ({
        primary: item.primary_emotion as any,
        secondary: item.secondary_emotion as any,
        intensity: item.intensity,
        timestamp: new Date(item.timestamp)
      }));
    } catch (error) {
      console.error('Failed to get moods:', error);
      return [];
    }
  }
  
  // Reports CRUD operations
  async saveReport(report: Report): Promise<void> {
    try {
      await this.db.withTransactionAsync(async () => {
        await this.db.execAsync(
          `INSERT OR REPLACE INTO reports (id, date, recipient, status, time_range, data)
           VALUES ('${this.escapeString(report.id)}', '${this.escapeString(report.date)}', 
                  '${this.escapeString(report.recipient)}', '${this.escapeString(report.status)}', 
                  '${this.escapeString(report.timeRange)}', 
                  '${this.escapeString(JSON.stringify(report.emotions))}')`
        );
      });
    } catch (error) {
      console.error('Failed to save report:', error);
      throw new Error('Could not save report data');
    }
  }
  
  async getReports(): Promise<Report[]> {
    try {
      const rawResults = await this.db.getAllAsync<{
        id: string;
        date: string;
        recipient: string;
        status: string;
        time_range: string;
        data: string;
      }>('SELECT * FROM reports ORDER BY date DESC');
      
      return (rawResults || []).map(item => {
        try {
          return {
            id: item.id,
            date: item.date,
            recipient: item.recipient,
            status: item.status as any,
            timeRange: item.time_range as any,
            emotions: JSON.parse(item.data)
          };
        } catch (parseError) {
          console.error('Failed to parse report data:', parseError);
          return {
            id: item.id,
            date: item.date,
            recipient: item.recipient,
            status: item.status as any,
            timeRange: item.time_range as any,
            emotions: {}
          };
        }
      });
    } catch (error) {
      console.error('Failed to get reports:', error);
      return [];
    }
  }
  
  // Clear all data
  async clearAllData(): Promise<void> {
    try {
      await this.db.withTransactionAsync(async () => {
        await this.db.execAsync('DELETE FROM recordings');
        await this.db.execAsync('DELETE FROM moods');
        await this.db.execAsync('DELETE FROM reports');
      });
    } catch (error) {
      console.error('Failed to clear data:', error);
      throw new Error('Could not clear database');
    }
  }
  
  // Helper method to escape strings for SQL queries
  private escapeString(value: string): string {
    if (!value) return '';
    // Replace single quotes with two single quotes to escape them in SQL
    return value.replace(/'/g, "''");
  }
}

export default new DatabaseService();
