#!/bin/bash

# Print a message indicating that the FastAPI server is starting
echo "Starting FastAPI server..."

# Start FastAPI using uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 80 --reload
