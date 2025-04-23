-- schema.sql

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Funds table - stores the main fund information
CREATE TABLE IF NOT EXISTS funds (
    fund_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    manager_name TEXT NOT NULL,
    description TEXT,
    nav REAL NOT NULL CHECK (nav >= 0),
    creation_date TEXT NOT NULL,  -- Stored as ISO8601 string format
    performance REAL NOT NULL,
    last_updated TEXT NOT NULL DEFAULT (DATETIME('now')),
    CONSTRAINT unique_fund_name UNIQUE (name)
);

-- Fund Managers table - stores detailed information about fund managers
CREATE TABLE IF NOT EXISTS fund_managers (
    manager_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    qualification TEXT,
    years_experience INTEGER CHECK (years_experience >= 0),
    date_joined TEXT NOT NULL DEFAULT (DATE('now'))
);

-- Fund Categories table - allows categorization of funds
CREATE TABLE IF NOT EXISTS fund_categories (
    category_id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- Fund-Category relationship table (many-to-many)
CREATE TABLE IF NOT EXISTS fund_category_mappings (
    fund_id TEXT,
    category_id TEXT,
    PRIMARY KEY (fund_id, category_id),
    FOREIGN KEY (fund_id) REFERENCES funds (fund_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES fund_categories (category_id) ON DELETE CASCADE
);

-- Fund Performance History table - tracks performance over time
CREATE TABLE IF NOT EXISTS fund_performance_history (
    history_id TEXT PRIMARY KEY,
    fund_id TEXT NOT NULL,
    performance_date TEXT NOT NULL,  -- Stored as ISO8601 date format
    performance_value REAL NOT NULL,
    FOREIGN KEY (fund_id) REFERENCES funds (fund_id) ON DELETE CASCADE,
    CONSTRAINT unique_fund_date UNIQUE (fund_id, performance_date)
);

-- Creating indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_funds_manager_name ON funds (manager_name);
CREATE INDEX IF NOT EXISTS idx_fund_performance_history_fund_id ON fund_performance_history (fund_id);
CREATE INDEX IF NOT EXISTS idx_fund_performance_history_date ON fund_performance_history (performance_date);