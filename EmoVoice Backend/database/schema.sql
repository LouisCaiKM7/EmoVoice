-- Users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    password_hash TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_login TEXT,
    preferences TEXT -- JSON string for user preferences
);

-- Recordings table
CREATE TABLE IF NOT EXISTS recordings (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    duration INTEGER, -- in seconds
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    file_path TEXT,
    file_size INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Emotions table
CREATE TABLE IF NOT EXISTS emotions (
    id TEXT PRIMARY KEY,
    recording_id TEXT NOT NULL,
    primary_emotion TEXT NOT NULL,
    secondary_emotion TEXT,
    primary_confidence REAL, -- 0.0 to 1.0
    secondary_confidence REAL, -- 0.0 to 1.0
    intensity REAL, -- 0.0 to 1.0
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recording_id) REFERENCES recordings(id)
);

-- Reports table
CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT,
    description TEXT,
    time_range TEXT NOT NULL, -- 'week', 'month', 'custom'
    start_date TEXT,
    end_date TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    data TEXT, -- JSON string of report data
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Report shares table
CREATE TABLE IF NOT EXISTS report_shares (
    id TEXT PRIMARY KEY,
    report_id TEXT NOT NULL,
    recipient_email TEXT NOT NULL,
    access_token TEXT NOT NULL,
    status TEXT DEFAULT 'pending', -- 'pending', 'viewed', 'expired'
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    expires_at TEXT,
    FOREIGN KEY (report_id) REFERENCES reports(id)
);

-- Insights table
CREATE TABLE IF NOT EXISTS insights (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT, -- 'trigger', 'pattern', 'tip'
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Smart home integrations table
CREATE TABLE IF NOT EXISTS smart_home_integrations (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    provider TEXT NOT NULL, -- 'philips_hue', 'google_home', etc.
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TEXT,
    settings TEXT, -- JSON string of integration settings
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);