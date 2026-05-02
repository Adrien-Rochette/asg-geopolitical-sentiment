CREATE TABLE IF NOT EXISTS headlines (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    confidence NUMERIC NOT NULL,
    source TEXT,
    region TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);