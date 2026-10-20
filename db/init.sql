CREATE TABLE IF NOT EXISTS places (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(255) NOT NULL,
    visited BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO places (name, visited) VALUES
    ('Tokio', FALSE),
    ('Budapest', TRUE),
    ('Londres', FALSE),
    ('Lisboa', TRUE),
    ('París', FALSE),
    ('Madrid', FALSE),
    ('Berlín', TRUE),
    ('Viena', FALSE),
    ('Estambul', TRUE),
    ('Oslo', FALSE),
    ('Zúrich', FALSE);