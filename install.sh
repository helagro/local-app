#!/bin/bash
set -e

SERVICE_NAME="local-app.service"
SYSTEMD_DIR="/etc/systemd/system"

# Stopping service
echo "Stopping existing service if running..."
sudo systemctl stop "$SERVICE_NAME" || true

# Check if service file exists
if [ ! -f "$SERVICE_NAME" ]; then
    echo "Error: $SERVICE_NAME not found in current directory."
    exit 1
fi

echo "Copying $SERVICE_NAME to $SYSTEMD_DIR..."
sudo cp "$SERVICE_NAME" "$SYSTEMD_DIR/"

echo "Setting correct permissions..."
sudo chmod 644 "$SYSTEMD_DIR/$SERVICE_NAME"

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling service to start on boot..."
sudo systemctl enable "$SERVICE_NAME"

echo "Starting service now..."
sudo systemctl start "$SERVICE_NAME"

echo "Done! Check status with:"
echo "  systemctl status $SERVICE_NAME"
