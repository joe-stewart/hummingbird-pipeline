#!/usr/bin/env bash
# deploy.sh — install hummingbird capture pipeline on Jetson
# Run from: ~/Development/hummer-capture/ on the Jetson as joe
# Usage: bash deploy.sh

set -euo pipefail

OPT_DIR="/opt/hummingbird"
FRAMES_DIR="$OPT_DIR/frames"
PYTHON="/opt/cv-env/bin/python3"
SERVICE_NAME="hummingbird"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
SCRIPT_SRC="$(dirname "$0")/capture.py"

echo "=== Hummingbird deploy ==="

# 1. Create system user if it doesn't exist
if ! id -u hummingbird &>/dev/null; then
    echo "[1/5] Creating hummingbird system user..."
    sudo useradd --system --no-create-home --shell /usr/sbin/nologin hummingbird
else
    echo "[1/5] User hummingbird already exists — skipping"
fi

# 2. Create /opt/hummingbird/frames
echo "[2/5] Creating $FRAMES_DIR..."
sudo mkdir -p "$FRAMES_DIR"
sudo chown -R hummingbird:hummingbird "$OPT_DIR"
sudo chmod 755 "$OPT_DIR"
sudo chmod 775 "$FRAMES_DIR"

# Allow joe to read/write frames without sudo
sudo usermod -aG hummingbird joe

# 3. Copy capture.py
echo "[3/5] Copying capture.py → $OPT_DIR/capture.py..."
sudo cp "$SCRIPT_SRC" "$OPT_DIR/capture.py"
sudo chown hummingbird:hummingbird "$OPT_DIR/capture.py"
sudo chmod 644 "$OPT_DIR/capture.py"

# 4. Write systemd service
echo "[4/5] Installing systemd service..."
sudo tee "$SERVICE_FILE" > /dev/null << SERVICE
[Unit]
Description=Hummingbird capture pipeline
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=hummingbird
Group=hummingbird
WorkingDirectory=/opt/hummingbird

ExecStartPre=/bin/sleep 5
ExecStart=$PYTHON /opt/hummingbird/capture.py

Restart=on-failure
RestartSec=10
StartLimitIntervalSec=120
StartLimitBurst=5

StandardOutput=journal
StandardError=journal
SyslogIdentifier=hummingbird

[Install]
WantedBy=multi-user.target
SERVICE

# 5. Reload and enable (but don't start)
echo "[5/5] Enabling service (not starting)..."
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"

echo ""
echo "=== Deploy complete ==="
echo ""
echo "To start:          sudo systemctl start hummingbird"
echo "To watch logs:     journalctl -u hummingbird -f"
echo "To check status:   systemctl status hummingbird"
echo "Frames saved to:   $FRAMES_DIR"
echo ""
echo "NOTE: log out and back in for group membership to take effect"
echo "      (so joe can read/write $FRAMES_DIR without sudo)"
