CREATE DATABASE meetings;

CREATE TABLE meetings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Scheduled'
);

CREATE TABLE participants (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES meetings(id),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES meetings(id),
    title VARCHAR(255) NOT NULL,
    expected_time INTEGER, -- Time in minutes
    owner_id INTEGER REFERENCES participants(id)
);

CREATE TABLE actions (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES meetings(id),
    description TEXT,
    responsible_id INTEGER REFERENCES participants(id),
    status VARCHAR(50) DEFAULT 'Open',
    target_date TIMESTAMP
);

CREATE TABLE risks (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER REFERENCES meetings(id),
    description TEXT,
    resolution VARCHAR(50) DEFAULT 'Mitigate',
    status VARCHAR(50) DEFAULT 'Open',
    responsible_id INTEGER REFERENCES participants(id)
);