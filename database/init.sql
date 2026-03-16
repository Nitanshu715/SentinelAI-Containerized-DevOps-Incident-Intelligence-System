CREATE TABLE IF NOT EXISTS incidents (
    id SERIAL PRIMARY KEY,
    service_name TEXT,
    severity TEXT,
    downtime_minutes INT,
    region TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);