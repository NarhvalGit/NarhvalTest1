#!/bin/bash
# Script to setup PostgreSQL database for the Prompt Agent application

echo "Setting up PostgreSQL database..."

# Create database (update credentials as needed)
PGPASSWORD=postgres psql -U postgres -h localhost -c "CREATE DATABASE prompt_agent_db;" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "Database 'prompt_agent_db' created successfully!"
else
    echo "Database might already exist or there was an error. Continuing..."
fi

echo "Database setup complete!"
