@echo off
echo PostgreSQL Password Reset Script
echo ================================

echo Step 1: Stop PostgreSQL Service
net stop postgresql-x64-15

echo Step 2: Start PostgreSQL in single user mode
echo Run this command manually:
echo psql -U postgres -d postgres

echo Step 3: Reset password with this SQL:
echo ALTER USER postgres PASSWORD 'newpassword';

echo Step 4: Restart PostgreSQL Service
net start postgresql-x64-15

pause