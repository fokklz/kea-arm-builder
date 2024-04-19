#!/bin/bash

# Define the screen session name
SESSION_NAME="kea_builder"

# Check if the session exists
if screen -list | grep -q "\.$SESSION_NAME"; then
    # Attach to the screen session with full control
    screen -r $SESSION_NAME
else
    echo "Screen session '$SESSION_NAME' not found. Please start the session first."
fi
