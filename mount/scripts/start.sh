#!/bin/bash

# Print a message indicating that the migration is starting
echo "Running Alembic migrations..."

# Run Alembic migrations to upgrade the database schema to the latest revision
alembic upgrade head

# Check if the migration was successful
if [ $? -ne 0 ]; then
  echo "Alembic migrations failed."
  # exit 1
fi

# Print a message indicating that the FastAPI server is starting
echo "Starting FastAPI server..."

# Start FastAPI using uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 80 --reload
