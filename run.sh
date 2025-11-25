#!/usr/bin/env bash
set -e
# Build image
docker build -t paletteviz:latest .
# Run container, mounting your local assets (optional) so you can swap images without rebuilding.
# The container will generate /app/output and serve it on port 8000.
docker run --rm -p 8000:8000 -v "$(pwd)/assets":/app/assets paletteviz:latest