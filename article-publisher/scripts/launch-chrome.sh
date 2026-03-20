#!/bin/bash
# Launch Chrome with the bo.bergstrom@gmail.com profile for article publishing.
# Uses the remote debugging port so Playwright MCP can connect.

CHROME_APP="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE_DIR="$HOME/Library/Application Support/Google/Chrome"
PROFILE_NAME="bo.bergstrom@gmail.com"
DEBUGGING_PORT=9222

# Find the correct profile directory by checking Local State
LOCAL_STATE="$PROFILE_DIR/Local State"

if [ -f "$LOCAL_STATE" ]; then
    # Extract profile directory for the matching email
    PROFILE_PATH=$(python3 -c "
import json, sys
with open('$LOCAL_STATE') as f:
    state = json.load(f)
profiles = state.get('profile', {}).get('info_cache', {})
for dir_name, info in profiles.items():
    if info.get('user_name', '') == '$PROFILE_NAME' or info.get('gaia_name', '') == '$PROFILE_NAME':
        print(dir_name)
        sys.exit(0)
# If email not found, try matching on name
for dir_name, info in profiles.items():
    if '$PROFILE_NAME' in info.get('user_name', '') or '$PROFILE_NAME' in info.get('gaia_name', ''):
        print(dir_name)
        sys.exit(0)
print('Default')
" 2>/dev/null)
else
    PROFILE_PATH="Default"
fi

echo "Using Chrome profile: $PROFILE_PATH"

# Check if Chrome is already running with debugging port
if lsof -i :$DEBUGGING_PORT >/dev/null 2>&1; then
    echo "Chrome already running with remote debugging on port $DEBUGGING_PORT"
    exit 0
fi

# Launch Chrome with the profile and remote debugging
"$CHROME_APP" \
    --profile-directory="$PROFILE_PATH" \
    --remote-debugging-port=$DEBUGGING_PORT \
    --no-first-run \
    --no-default-browser-check \
    &>/dev/null &

# Wait for Chrome to be ready
echo "Launching Chrome..."
for i in $(seq 1 15); do
    if lsof -i :$DEBUGGING_PORT >/dev/null 2>&1; then
        echo "Chrome is ready on port $DEBUGGING_PORT"
        exit 0
    fi
    sleep 1
done

echo "Warning: Chrome may not have started correctly. Check manually."
exit 1
