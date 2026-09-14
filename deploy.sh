#!/bin/bash
set -e

echo "======================================"
echo "    Deploying NORVAULT to Production  "
echo "======================================"

# Ensure Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker and Docker Compose."
    exit 1
fi

echo "1. Pulling latest changes (if in a git repo)..."
git pull origin main || true

echo "2. Building and starting containers in detached mode..."
docker-compose up -d --build

echo "3. Pruning old unused images to save space..."
docker image prune -f

echo "======================================"
echo " Deployment Successful!"
echo " Frontend: http://localhost:3000 (Mapped from port 80)"
echo " Backend API: http://localhost:8000"
echo "======================================"
