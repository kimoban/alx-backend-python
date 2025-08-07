#!/bin/bash

# Docker Build and Test Script for Messaging App

echo "=== Docker Build and Test Script ==="
echo "Messaging App Container Setup"
echo ""

# Check if Docker is running
echo "🔍 Checking Docker availability..."
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

echo "✅ Docker is running!"
echo ""

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -t messaging-app -f ./messaging_app/Dockerfile .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi

echo ""

# Run the container
echo "🚀 Starting container..."
echo "The application will be available at http://localhost:8000"
echo "Press Ctrl+C to stop the container"
echo ""

docker run -p 8000:8000 \
    -e DEBUG=True \
    -e SECRET_KEY=django-insecure-docker-development-key \
    -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0 \
    messaging-app
