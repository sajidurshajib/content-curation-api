#!/bin/bash

# Check if the correct number of arguments were passed
if [ "$#" -ne 1 ]; then
    echo "$#"
    echo "Usage: $0 <migration_name>"
    exit 1
fi

MIGRATION_NAME=$1

# Run Alembic command to create a new migration file
echo "Creating new Alembic migration file with name: $MIGRATION_NAME"
alembic revision --autogenerate -m "$MIGRATION_NAME"

# Check if the Alembic command was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to create migration file."
    exit 1
fi

echo "Migration file created successfully."
