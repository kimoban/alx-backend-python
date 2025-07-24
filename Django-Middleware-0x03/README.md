# Django Messaging App with Advanced Middleware

## 🚀 Overview

A comprehensive RESTful API for user messaging built with Django and Django REST Framework (DRF). This project demonstrates advanced middleware patterns, security features, and robust API design principles.

## ✨ Features

### Core Functionality

- 🔐 User authentication and authorization
- 👥 Conversation management between users
- 💬 Real-time message sending within conversations
- 🛡️ Role-based access control (Admin, Moderator, User)
- 📊 RESTful API endpoints for all operations

### Advanced Middleware

- 📝 **Request Logging**: Comprehensive request tracking with timestamps
- ⏰ **Time-based Access Control**: Restrict messaging to business hours (6 AM - 9 PM)
- 🚦 **Rate Limiting**: IP-based throttling (5 messages per minute)
- 🔒 **Role Permission Control**: Admin/Moderator access restrictions

## 🛠️ Technologies

- **Backend**: Python 3.13+, Django 5.2.4
- **API Framework**: Django REST Framework 3.16.0
- **Database**: SQLite (default), PostgreSQL (production-ready)
- **Environment Management**: django-environ
- **Filtering**: django-filter

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kimoban/alx-backend-python.git
cd Django-Middleware-0x03
```

### 2. Virtual Environment Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

```bash
# Apply migrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 🔗 API Endpoints

### Authentication Endpoints

- `POST /admin/` - Admin interface access
- `GET /api-auth/login/` - Login interface

### Conversation Management

- `GET /api/v1/conversations/` - List user's conversations
- `POST /api/v1/conversations/` - Create new conversation
- `GET /api/v1/conversations/{id}/` - Retrieve specific conversation
- `PUT /api/v1/conversations/{id}/` - Update conversation
- `DELETE /api/v1/conversations/{id}/` - Delete conversation

### Message Operations

- `GET /api/v1/messages/` - List messages in user's conversations
- `POST /api/v1/messages/` - Send new message
- `GET /api/v1/messages/{id}/` - Retrieve specific message
- `PUT /api/v1/messages/{id}/` - Update message
- `DELETE /api/v1/messages/{id}/` - Delete message

## 🔐 Authentication & Authorization

### Authentication Methods

- **Session Authentication** (default)
- **Token Authentication** (available)
- **Admin Interface** - Full Django admin access

### User Roles

- **Admin**: Full system access, can manage all users and content
- **Moderator**: Limited administrative access, content moderation
- **User**: Basic messaging functionality

### Permission Levels

- Unauthenticated users: Read-only access to public endpoints
- Authenticated users: Full messaging capabilities within time restrictions
- Admin/Moderator: Unrestricted access to protected endpoints

## 🛡️ Middleware Security Features

### 1. Request Logging Middleware

- **Location**: `logs/requests.log`
- **Format**: `TIMESTAMP - User: USERNAME - Path: REQUEST_PATH`
- **Purpose**: Security auditing and debugging

### 2. Time-based Access Control

- **Restriction**: Messaging blocked outside 6:00 AM - 9:00 PM
- **Response**: HTTP 403 Forbidden
- **Scope**: Only affects messaging endpoints

### 3. Rate Limiting

- **Limit**: 5 POST requests per minute per IP
- **Response**: HTTP 429 Too Many Requests
- **Scope**: Message creation endpoints only

### 4. Role Permission Control

- **Protected Actions**: Admin-only operations
- **Response**: HTTP 403 Forbidden for unauthorized users
- **Scope**: Administrative and moderation endpoints

## 🧪 Testing

### Run Test Suite

```bash
python manage.py test
```

### Test Middleware Functionality

```bash
# Test rate limiting
python test_rate_limiting.py

# Test middleware summary
python middleware_summary.py
```

### Manual Testing

1. **Rate Limiting**: Make 6 POST requests to `/api/v1/messages/` rapidly
2. **Time Restriction**: Access messaging outside 6 AM - 9 PM
3. **Role Permissions**: Access admin endpoints without proper role
4. **Request Logging**: Check `logs/requests.log` for logged requests

## 📁 Project Structure

Django-Middleware-0x03/  
├── chats/                      # Main application  
│   ├── middleware.py          # Custom middleware classes  
│   ├── models.py             # User, Conversation, Message models  
│   ├── views.py              # API viewsets  
│   ├── serializers.py        # DRF serializers  
│   ├── urls.py               # URL routing  
│   └── admin.py              # Admin interface configuration  
├── Django-Middleware-0x03/    # Project settings  
│   ├── settings.py           # Django configuration  
│   ├── urls.py               # Root URL configuration  
│   └── wsgi.py               # WSGI application  
├── logs/                      # Log files  
│   └── requests.log          # Request logging output  
├── manage.py                  # Django management script  
├── requirements.txt          # Python dependencies  
└── README.md                 # This file  

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=your-db-host
DB_PORT=your-db-port
```

### Middleware Configuration

The middleware stack is configured in `settings.py`:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "chats.middleware.RolePermissionMiddleware",      # Role-based access
    "chats.middleware.OffensiveLanguageMiddleware",   # Rate limiting
    "chats.middleware.RestrictAccessByTimeMiddleware", # Time restrictions
    "chats.middleware.RequestLoggingMiddleware",      # Request logging
]
```

## 🚀 Production Deployment

### Database Configuration

For production, update `settings.py` to use PostgreSQL:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}
```

### Security Considerations

- Set `DEBUG = False` in production
- Use secure secret key generation
- Configure HTTPS/SSL certificates
- Set up proper CORS headers
- Implement proper logging and monitoring

## 📊 Monitoring & Logging

### Request Logs

- **File**: `logs/requests.log`
- **Format**: Timestamp, User, Request Path
- **Rotation**: Manual (implement logrotate for production)

### Error Handling

- Custom error pages for 403, 404, 429, 500
- Detailed error messages in development
- Sanitized error responses in production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation for API changes
- Ensure middleware changes don't break existing functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**Server won't start:**

- Check if all dependencies are installed
- Verify database migrations are applied
- Ensure port 8000 is not in use

**Middleware errors:**

- Check middleware order in `settings.py`
- Verify all custom middleware classes are properly imported
- Review middleware logs in `logs/requests.log`

**API access issues:**

- Verify authentication credentials
- Check user roles and permissions
- Ensure requests are within allowed time windows
- Check rate limiting status

### Support

For issues and questions:

- 📧 Open an issue on GitHub
- 📝 Check the documentation
- 💬 Contact the development team

## 🙏 Acknowledgments

- Django and Django REST Framework communities
- ALX Backend Python curriculum
- Contributors and maintainers

---

## Built with ❤️ for learning advanced Django middleware patterns
