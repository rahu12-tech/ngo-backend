-- PostgreSQL Database Setup
-- Run this in pgAdmin or psql command line

-- Create database
CREATE DATABASE ngo_db;

-- Create user (optional, you can use default postgres user)
CREATE USER ngo_user WITH PASSWORD 'ngo123';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE ngo_db TO ngo_user;

-- Connect to ngo_db and grant schema privileges
\c ngo_db;
GRANT ALL ON SCHEMA public TO ngo_user;