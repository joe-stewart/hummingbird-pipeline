#!/usr/bin/env bash
# setup.sh — hummingbird-pipeline setup and maintenance
#
# First run (no config.env):   creates config.env stub, prints instructions
# Second run (config.env exists): validates, pings devices, generates files
# Admin run (bin/ exists):     make clean && make, ansible ping all devices

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="$REPO_ROOT/config.env"
BIN="$REPO_ROOT/bin"
MAKEFILE="$BIN/Makefile"
INVENTORY="$HOME/ansible/inventory.ini"

# ── Admin path ────────────────────────────────────────────────────────────────
if [ -d "$BIN" ]; then
    echo "→ admin mode: refreshing generated files..."
    make -C "$BIN" clean && make -C "$BIN"
    echo ""
    if command -v ansible &>/dev/null && [ -f "$INVENTORY" ]; then
        ansible-playbook -i "$INVENTORY" "$HOME/hummingbird-pipeline/ansible/health.yml"
    else
        echo "  (ansible not found or inventory not generated — skipping ping)"
    fi
    echo ""
    echo "✓ done"
    exit 0
fi

# ── Second pass — config.env exists ──────────────────────────────────────────
if [ -f "$CONFIG" ]; then
    echo "→ config.env found — validating..."
    echo ""

    MISSING=0
    while IFS= read -r line; do
        [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue
        key="${line%%=*}"
        val="${line#*=}"
        if [ -z "$val" ]; then
            echo "  ✗ $key is not set"
            MISSING=$((MISSING + 1))
        fi
    done < "$CONFIG"

    if [ "$MISSING" -gt 0 ]; then
        echo ""
        echo "  Fill in the missing values in config.env and re-run setup.sh"
        exit 1
    fi

    echo "  all variables set"
    echo ""
    echo "→ pinging devices..."
    source "$CONFIG"
    for var in RECAMERA_IP JETSON_IP RPI2_IP ARDUINO_IP BERYL_IP; do
        ip="${!var}"
        if ping -c1 -W2 "$ip" &>/dev/null; then
            echo "  ✓ $var ($ip) reachable"
        else
            echo "  ✗ $var ($ip) unreachable"
        fi
    done

    echo ""
    echo "→ generating config files..."
    mkdir -p "$REPO_ROOT/generated"
    while IFS= read -r line; do
        [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue
        export "${line%%=*}=${line#*=}"
    done < "$CONFIG"

    for tmpl in jetson/capture.py recamera/bird_watch.py recamera/wpa_supplicant.conf \
                ansible/inventory.ini arduino/firmware/bird_count/arduino_secrets.h \
                docs/architecture.md docs/decisions.md docs/devices.md docs/models.md; do
        outfile="$REPO_ROOT/generated/$tmpl"
        mkdir -p "$(dirname "$outfile")"
        envsubst < "$REPO_ROOT/$tmpl" > "$outfile"
        echo "  rendered $tmpl"
    done

    echo ""
    echo "✓ generated files are in generated/ — review before deploying"
    echo ""
    echo "Next steps:"
    echo "  Jetson  : scp generated/jetson/capture.py joe@<jetson>:~/Development/hummer-capture/"
    echo "  reCamera: scp generated/recamera/bird_watch.py recamera:/userdata/"
    echo "  reCamera: scp generated/recamera/wpa_supplicant.conf recamera:/etc/wpa_supplicant/"
    echo "  Arduino : copy generated/arduino/firmware/bird_count/arduino_secrets.h to your sketch folder"
    exit 0
fi

# ── First pass — no config.env ────────────────────────────────────────────────
echo "Hummingbird Pipeline Setup"
echo "=========================="
echo ""
echo "No config.env found — creating stub..."
echo ""

cat > "$CONFIG" << 'EOF'
# config.env — fill in values for your network then re-run setup.sh

# Device IPs
RECAMERA_IP=
JETSON_IP=
RPI2_IP=
ARDUINO_IP=
NUC_IP=
M4_IP=
BERYL_IP=
SWITCH_IP=

# Subnets
SUBNET_LAN=
SUBNET_OPT1=

# Ports (defaults shown)
RECAMERA_WS_PORT=8090
NTFY_PORT=8080

# Paths
FRAMES_DIR=
HUMMINGBIRD_DIR=

# WiFi credentials (for reCamera and Arduino)
WIFI_SSID=
WIFI_PASS=
EOF

echo "Created config.env — fill in your values and re-run: bash setup.sh"
echo ""
echo "To see all files requiring configuration:"
echo "  grep -r '\${' --include='*.py' --include='*.conf' --include='*.ini' --include='*.h' . | grep -v bin/"
