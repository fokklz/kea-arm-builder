#!/bin/bash

# Define the path to the project directory
PROJECT_DIR="/opt/kea-arm-builder"

# Navigate to the project directory
cd $PROJECT_DIR

# Define the session name
SESSION_NAME="kea_builder"

# Check if the screen session already exists
if screen -list | grep -q "\.${SESSION_NAME}\s"; then
    echo "Session $SESSION_NAME already exists. Exiting."
    exit 1
else
    # Clear log
    echo "" > "${SESSION_NAME}.log"
    # Command to start a detached screen session and log screen output
    screen -L -Logfile "${SESSION_NAME}.log" -dmS $SESSION_NAME bash -c 'source .venv/bin/activate && python main.py'
    echo "Session $SESSION_NAME started."
fi
