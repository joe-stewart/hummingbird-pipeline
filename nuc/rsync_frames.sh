#!/usr/bin/env bash
# rsync_frames.sh — pull latest captures from Jetson to NUC
# Run from NUC as joe
# Usage: bash rsync_frames.sh

JETSON="joe@192.168.2.8"
REMOTE="/opt/hummingbird/frames/"
LOCAL="$(dirname "$0")/frames/"

mkdir -p "$LOCAL"
rsync -av --progress "$JETSON:$REMOTE" "$LOCAL"
echo "Frames synced to $LOCAL"
