# Docker Build and Test Script for Messaging App (PowerShell)

Write-Host "=== Docker Build and Test Script ===" -ForegroundColor Cyan
Write-Host "Messaging App Container Setup" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "🔍 Checking Docker availability..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop and try again." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Build the Docker image
Write-Host "🔨 Building Docker image..." -ForegroundColor Yellow
docker build -t messaging-app -f .\messaging_app\Dockerfile .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker image built successfully!" -ForegroundColor Green
}
else {
    Write-Host "❌ Failed to build Docker image" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Run the container
Write-Host "🚀 Starting container..." -ForegroundColor Yellow
Write-Host "The application will be available at http://localhost:8000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the container" -ForegroundColor Cyan
Write-Host ""

docker run -p 8000:8000 `
    -e DEBUG=True `
    -e SECRET_KEY=django-insecure-docker-development-key `
    -e DJANGO_ALLOWED_HOSTS=localhost, 127.0.0.1, 0.0.0.0 `
    messaging-app
