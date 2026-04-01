#!/usr/bin/env bash
set -euo pipefail

# Example: start recording and switch to the "super" mode key.
/usr/bin/open -g "superwhisper://record"
sleep 0.15
/usr/bin/open -g "superwhisper://mode?key=super"

