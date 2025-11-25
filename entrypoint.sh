#!/usr/bin/env bash
set -euo pipefail

# Allow overriding via env
INPUT_IMAGE=${INPUT_IMAGE:-/app/assets/sample.jpg}
OUTDIR=${OUTDIR:-/app/output}
COLORS=${COLORS:-6}

if [ ! -f "$INPUT_IMAGE" ]; then
  echo "ERROR: input image not found at $INPUT_IMAGE"
  echo "Place a sample image at assets/sample.jpg or mount one with -v"
  exec "$@"
fi

echo "Generating palette & histogram from $INPUT_IMAGE -> $OUTDIR"
python /app/src/palette.py "$INPUT_IMAGE" "$OUTDIR" --colors "$COLORS"

# Serve the output directory via a simple static server
echo "Serving results at http://0.0.0.0:8000 (output dir: $OUTDIR)"
cd "$OUTDIR"
python -m http.server 8000 --bind 0.0.0.0
