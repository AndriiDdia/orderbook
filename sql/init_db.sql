-- CREATE DATABASE IF NOT EXISTS crypto;

-- Switch to the newly created database
\c crypto;


CREATE TABLE IF NOT EXISTS order_book (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL,
    observe_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    order_type VARCHAR(50) NOT NULL,
    price NUMERIC(18, 4) NOT NULL,
    amount NUMERIC(18, 4) NOT NULL
);
