import { Report, EmotionType } from '../types';
import DatabaseService from './DatabaseService';
import ApiService from './ApiService';

class ReportService {
  // Generate a new report
  async generateReport(timeRange: 'week' | 'month' | 'custom', startDate?: Date, endDate?: Date): Promise<Report> {
    // Get recordings from database
    const recordings = await DatabaseService.getRecordings();
    
    // Filter recordings by date range
    const filteredRecordings = this.filterRecordingsByDateRange(
      recordings, 
      timeRange, 
      startDate, 
      endDate
    );
    
    // Aggregate emotions data
    const emotions = this.aggregateEmotions(filteredRecordings);
    
    // Create report
    const report: Report = {
      id: Date.now().toString(),
      date: new Date().toISOString(),
      recipient: '',
      status: 'Pending',
      timeRange,
      emotions
    };
    
    // Save report to database
    await DatabaseService.saveReport(report);
    
    return report;
  }
  
  // Share report with a professional
  async shareReport(reportId: string, recipient: string): Promise<boolean> {
    try {
      // Get report from database
      const reports = await DatabaseService.getReports();
      const report = reports.find(r => r.id === reportId);
      
      if (!report) return false;
      
      // Update report
      report.recipient = recipient;
      report.status = 'Shared';
      
      // Save updated report
      await DatabaseService.saveReport(report);
      
      // Share with API
      const success = await ApiService.shareReport(report);
      
      return success;
    } catch (error) {
      console.error('Error sharing report:', error);
      return false;
    }
  }
  
  // Helper method to filter recordings by date range
  private filterRecordingsByDateRange(recordings: any[], timeRange: string, startDate?: Date, endDate?: Date) {
    const now = new Date();
    let start: Date;
    
    if (timeRange === 'week') {
      // Last 7 days
      start = new Date(now);
      start.setDate(now.getDate() - 7);
    } else if (timeRange === 'month') {
      // Last 30 days
      start = new Date(now);
      start.setDate(now.getDate() - 30);
    } else if (timeRange === 'custom' && startDate && endDate) {
      // Custom date range
      start = startDate;
      now.setHours(23, 59, 59, 999);
      return recordings.filter(recording => {
        const recordingDate = new Date(recording.date);
        return recordingDate >= start && recordingDate <= endDate;
      });
    } else {
      // Default to last 7 days
      start = new Date(now);
      start.setDate(now.getDate() - 7);
    }
    
    // Filter recordings
    return recordings.filter(recording => {
      const recordingDate = new Date(recording.date);
      return recordingDate >= start && recordingDate <= now;
    });
  }
  
  // Helper method to aggregate emotions data
  private aggregateEmotions(recordings: any[]) {
    const emotions: { [key in EmotionType]?: number[] } = {};
    
    // Initialize emotions object
    const emotionTypes: EmotionType[] = ['Joy', 'Sadness', 'Anger', 'Fear', 'Surprise', 'Disgust', 'Calm'];
    emotionTypes.forEach(emotion => {
      emotions[emotion] = [];
    });
    
    // Aggregate emotions
    recordings.forEach(recording => {
      if (emotions[recording.emotion as EmotionType]) {
        emotions[recording.emotion as EmotionType]?.push(recording.intensity);
      }
    });
    
    return emotions;
  }
}

export default new ReportService();