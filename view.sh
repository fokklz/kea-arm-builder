#!/bin/bash

# Define the path to the log file
LOG_FILE="/opt/kea-arm-builder/kea_builder.log"

# Check if the log file exists
if [ -f "$LOG_FILE" ]; then
    # Follow the log file
    tail -f $LOG_FILE
else
    echo "Log file not found. Please check if the path is correct and the application is running."
fi
