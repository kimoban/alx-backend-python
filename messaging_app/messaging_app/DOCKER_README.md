# Docker Setup for Messaging App

This guide will help you set up and run the Django messaging app using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (usually comes with Docker Desktop)

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Clone the repository and navigate to the messaging app directory:**

   ```bash
   cd messaging_app
   ```

2. **Build and run with Docker Compose:**

   ```bash
   docker-compose up --build
   ```

3. **Access the application:**

   - Web App: [http://localhost:8000](http://localhost:8000)
   - Admin Panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)
   - API: [http://localhost:8000/api/](http://localhost:8000/api/)

4. **Default superuser credentials:**
   - Username: `admin`
   - Password: `admin123`

### Option 2: Using Docker directly

1. **Build the Docker image:**

   ```bash
   docker build -t messaging-app .
   ```

2. **Run the container:**

   ```bash
   docker run -p 8000:8000 \
     -e DEBUG=True \
     -e SECRET_KEY=django-insecure-docker-development-key \
     -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0 \
     messaging-app
   ```

## Environment Variables

The following environment variables can be set:

- `DEBUG`: Set to `True` for development, `False` for production
- `SECRET_KEY`: Django secret key (change in production)
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DB_NAME`: Database name (for PostgreSQL)
- `DB_USER`: Database user (for PostgreSQL)
- `DB_PASSWORD`: Database password (for PostgreSQL)
- `DB_HOST`: Database host (for PostgreSQL)
- `DB_PORT`: Database port (for PostgreSQL)

## Development with Docker

### Running commands inside the container

```bash
# Access the container shell
docker-compose exec web bash

# Run Django management commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic
```

### Viewing logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs web
```

### Stopping the application

```bash
# Stop and remove containers
docker-compose down

# Stop, remove containers and volumes
docker-compose down -v
```

## Production Deployment

For production deployment, consider:

1. **Update environment variables:**
   - Set `DEBUG=False`
   - Use a strong `SECRET_KEY`
   - Configure proper `DJANGO_ALLOWED_HOSTS`
   - Set up PostgreSQL database credentials

2. **Use a production WSGI server:**
   The Dockerfile can be modified to use Gunicorn instead of the development server.

3. **Set up proper volume mounts:**
   Mount persistent storage for database and media files.

4. **Configure reverse proxy:**
   Use Nginx or similar for serving static files and SSL termination.

## API Endpoints

Once running, you can access the following API endpoints:

### Authentication

- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/refresh/` - Token refresh
- `GET /api/auth/profile/` - User profile

### Conversations

- `GET /api/conversations/` - List conversations
- `POST /api/conversations/` - Create conversation
- `GET /api/conversations/{id}/` - Get conversation details

### Messages

- `GET /api/messages/` - List messages
- `POST /api/messages/` - Send message

## Troubleshooting

### Common Issues

1. **Port already in use:**

   ```bash
   # Change the port mapping in docker-compose.yml
   ports:
     - "8001:8000"  # Use port 8001 instead
   ```

2. **Database connection issues:**
   - Ensure PostgreSQL container is running
   - Check database credentials in environment variables

3. **Permission issues:**
   - The Dockerfile creates a non-root user for security
   - Ensure proper file permissions if mounting volumes

### Useful Commands

```bash
# Remove all containers and images
docker system prune -a

# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View images
docker images

# Remove specific image
docker rmi messaging-app
```

## File Structure

```bash
messaging_app/
├── messaging_app/
│   └── Dockerfile          # Docker configuration
├── docker-compose.yml      # Multi-container configuration
├── entrypoint.sh           # Container startup script
├── requirements.txt        # Python dependencies
├── .dockerignore           # Files to exclude from Docker build
└── DOCKER_README.md        # This file
```
