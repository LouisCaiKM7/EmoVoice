// Date formatting and manipulation utilities

/**
 * Format a date to a readable string
 */
export const formatDate = (date: Date): string => {
  const now = new Date();
  const yesterday = new Date(now);
  yesterday.setDate(yesterday.getDate() - 1);
  
  if (isSameDay(date, now)) {
    return `Today, ${formatTime(date)}`;
  } else if (isSameDay(date, yesterday)) {
    return `Yesterday, ${formatTime(date)}`;
  } else {
    return `${date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}, ${formatTime(date)}`;
  }
};

/**
 * Format time to 12-hour format
 */
export const formatTime = (date: Date): string => {
  return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
};

/**
 * Check if two dates are the same day
 */
export const isSameDay = (date1: Date, date2: Date): boolean => {
  return (
    date1.getFullYear() === date2.getFullYear() &&
    date1.getMonth() === date2.getMonth() &&
    date1.getDate() === date2.getDate()
  );
};

/**
 * Get start and end dates for a week
 */
export const getWeekDates = (date: Date = new Date()): { start: Date; end: Date } => {
  const day = date.getDay();
  const diff = date.getDate() - day + (day === 0 ? -6 : 1); // Adjust when day is Sunday
  
  const start = new Date(date);
  start.setDate(diff);
  start.setHours(0, 0, 0, 0);
  
  const end = new Date(start);
  end.setDate(end.getDate() + 6);
  end.setHours(23, 59, 59, 999);
  
  return { start, end };
};

/**
 * Format a week range as a string
 */
export const formatWeekRange = (date: Date = new Date()): string => {
  const { start, end } = getWeekDates(date);
  
  const startStr = start.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  const endStr = end.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  
  return `${startStr} - ${endStr}`;
};

/**
 * Get previous week's date
 */
export const getPreviousWeek = (date: Date): Date => {
  const newDate = new Date(date);
  newDate.setDate(newDate.getDate() - 7);
  return newDate;
};

/**
 * Get next week's date
 */
export const getNextWeek = (date: Date): Date => {
  const newDate = new Date(date);
  newDate.setDate(newDate.getDate() + 7);
  return newDate;
};

/**
 * Format seconds to MM:SS
 */
export const formatDuration = (seconds: number): string => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
};