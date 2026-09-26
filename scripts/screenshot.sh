#!/usr/bin/env bash
# Capture every page at desktop and mobile width, reporting console errors and
# horizontal overflow. Restarts the dev server first: DEBUG=False makes Django
# cache templates, so a long-running server serves stale HTML after an edit.
#
# One-time setup (Playwright's Chromium, ~100MB, cached outside the repo):
#   npx --yes playwright@1.49.1 install chromium
#   mkdir -p ~/.cache/wisdomcc-shots && cd ~/.cache/wisdomcc-shots \
#     && npm init -y && npm install playwright@1.49.1
#
# Usage: scripts/screenshot.sh [output-dir]   (default: .screenshots/)
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:-$REPO/.screenshots}"
PORT=8001
NODE_MODULES="$HOME/.cache/wisdomcc-shots/node_modules"

if [ ! -d "$NODE_MODULES/playwright" ]; then
  echo "Playwright not installed. See the setup comment at the top of this script." >&2
  exit 1
fi

lsof -ti:$PORT -sTCP:LISTEN 2>/dev/null | xargs -r kill || true
sleep 1
cd "$REPO"
nohup ./venv/bin/python manage.py runserver $PORT --insecure --noreload >/tmp/wisdomcc-shots.log 2>&1 &
trap 'lsof -ti:'$PORT' -sTCP:LISTEN 2>/dev/null | xargs -r kill || true' EXIT
timeout 40 bash -c "until curl -sf -o /dev/null http://127.0.0.1:$PORT/; do sleep 1; done"

mkdir -p "$OUT"
rm -f "$OUT"/*.png
NODE_PATH="$NODE_MODULES" SHOT="$OUT" BASE="http://127.0.0.1:$PORT" \
  node "$REPO/scripts/screenshot.mjs"
echo "Screenshots written to $OUT"
