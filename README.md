# ALX Backend Python - Advanced Python Development Portfolio

<!-- Centered badges (remove HTML for Markdown lint compliance) -->

<p align="center">

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2.4-green?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16.0-red?logo=django&logoColor=white)
![Testing](https://img.shields.io/badge/Testing-unittest-orange)
![Async](https://img.shields.io/badge/Async-asyncio-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

<!-- End centered badges -->

## 🎯 Project Overview

A comprehensive collection of advanced Python backend development projects showcasing modern software engineering practices, design patterns, and frameworks. This repository demonstrates expertise in Python development through practical implementations of testing, web development, asynchronous programming, and advanced language features.

## 📂 Project Structure

```
alx-backend-python/
├── 0x03-Unittests_and_integration_tests/    # Testing fundamentals & best practices
├── Django-Middleware-0x03/                  # Advanced Django middleware & security
├── messaging_app/                           # RESTful API development with DRF
├── python-context-async-operations-0x02/    # Context managers & async programming
├── python-decorators-0x01/                  # Advanced decorator patterns
├── python-generators-0x00/                  # Memory-efficient data processing
└── README.md                                # This comprehensive guide
```

## 🚀 Sub-Projects Overview

### 🧪 [0x03-Unittests_and_integration_tests](./0x03-Unittests_and_integration_tests/)

**Focus**: Testing Excellence & Quality Assurance

A comprehensive testing project demonstrating professional testing methodologies using Python's `unittest` framework.

#### Key Features: Unittests and Integration Tests

- ✅ **Unit Testing**: Isolated component testing with comprehensive mocking
- ✅ **Integration Testing**: End-to-end workflow validation
- ✅ **Parameterized Tests**: Data-driven testing approaches
- ✅ **Mock Strategies**: External dependency isolation
- ✅ **GitHub API Client**: Real-world testing scenarios

#### Technologies Used in Testing

- Python 3.7+
- unittest framework
- unittest.mock
- requests library
- GitHub API integration

#### Files (Testing Project)

- `client.py` - GitHub API client implementation
- `utils.py` - Utility functions with nested data access
- `fixtures.py` - Test data and mock responses
- `test_client.py` - Client integration tests
- `test_utils.py` - Utility function unit tests

**Learning Outcomes**: Professional testing practices, mocking strategies, test isolation, and quality assurance methodologies.

### 🛡️ [Django-Middleware-0x03](./Django-Middleware-0x03/)

**Focus**: Advanced Django Middleware & Security

A sophisticated Django messaging application showcasing enterprise-level middleware patterns and security implementations.

#### Key Features: Django Middleware

- 🔐 **Advanced Authentication**: JWT-based user authentication
- 📝 **Request Logging**: Comprehensive request tracking middleware
- ⏰ **Time-based Access Control**: Business hours restrictions
- 🚦 **Rate Limiting**: IP-based request throttling
- 🔒 **Role-based Permissions**: Admin/Moderator access control
- 📊 **RESTful API**: Complete CRUD operations

#### Technologies Used in Django Middleware

- Python 3.13+
- Django 5.2.4
- Django REST Framework 3.16.0
- SQLite/PostgreSQL
- Custom middleware implementation

#### Architecture

```
Django-Middleware-0x03/
├── chats/                    # Main application
│   ├── models.py            # User, Conversation, Message models
│   ├── views.py             # API viewsets and endpoints
│   ├── serializers.py       # DRF serializers
│   ├── middleware.py        # Custom middleware implementations
│   └── permissions.py       # Custom permission classes
├── middleware.py            # Global middleware configurations
├── settings.py              # Django settings with middleware
└── logs/                    # Request logging directory
```

#### Middleware Implementations

1. **Request Logging Middleware**: Tracks all incoming requests with timestamps
2. **Time Restriction Middleware**: Enforces business hours (6 AM - 9 PM)
3. **Rate Limiting Middleware**: Prevents spam (5 messages/minute per IP)
4. **Role Permission Middleware**: Admin/Moderator access control

**Learning Outcomes**: Django middleware development, security patterns, API design, and enterprise application architecture.

### 💬 [messaging_app](./messaging_app/)

**Focus**: RESTful API Development with Django REST Framework

A clean, well-structured messaging API demonstrating modern web API development practices.

#### Key Features: Messaging App

- 👥 **User Management**: Registration, authentication, profiles
- 💬 **Conversations**: Multi-user conversation management
- 📨 **Messaging**: Real-time message exchange
- 🔐 **Authentication**: Token-based API authentication
- 📖 **API Documentation**: Comprehensive endpoint documentation

#### API Endpoints

```
Authentication:
POST /api/auth/login/          # User login
POST /api/auth/register/       # User registration

Conversations:
GET /api/conversations/        # List user conversations
POST /api/conversations/       # Create new conversation
GET /api/conversations/{id}/   # Get conversation details

Messages:
POST /api/conversations/{id}/messages/  # Send message
GET /api/conversations/{id}/messages/   # Get conversation messages
```

#### Technologies

- Django 4.x
- Django REST Framework
- SQLite (development) / PostgreSQL (production)
- Token authentication

**Learning Outcomes**: REST API design, DRF implementation, authentication systems, and API documentation.

---

### ⚡ [python-context-async-operations-0x02](./python-context-async-operations-0x02/)

**Focus**: Context Managers & Asynchronous Programming

Advanced Python programming demonstrating context managers and async operations for efficient resource management.

#### Key Features: Context Managers & Async Operations

- 🔄 **Context Managers**: Custom context manager implementations
- ⚡ **Async Operations**: High-performance asynchronous database operations
- 🏃‍♂️ **Concurrent Execution**: Parallel task execution
- 🗄️ **Database Management**: Safe connection handling

#### Files (Context & Async Operations)

- `0-databaseconnection.py` - Custom database context manager
- `1-execute.py` - Query execution context manager
- `3-concurrent.py` - Async database operations with aiosqlite

#### Example Usage: Context Managers & Async Operations

```python
# Context Manager
with DatabaseConnection('example.db') as conn:
    # Automatic connection management
    cursor = conn.execute("SELECT * FROM users")

# Async Operations
async def fetch_data():
    async with aiosqlite.connect('db.sqlite') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()
```

**Learning Outcomes**: Resource management, async programming patterns, context manager protocols, and performance optimization.

### 🎨 [python-decorators-0x01](./python-decorators-0x01/)

**Focus**: Advanced Decorator Patterns & Database Operations

Sophisticated decorator implementations for database operations, logging, transactions, and resilience patterns.

#### Key Features: Decorators & Database Operations

- 📝 **Query Logging**: Automatic SQL query logging with timestamps
- 🔗 **Connection Management**: Automatic database connection handling
- 🔄 **Transaction Management**: Atomic database operations
- 🔁 **Retry Logic**: Automatic retry on failure with exponential backoff
- 💾 **Query Caching**: Intelligent query result caching

#### Decorator Implementations

1. **@log_queries**: Logs all database queries with execution time

```python
@log_queries
def fetch_users(query):
    # Automatically logs query execution
```

2. **@with_db_connection**: Manages database connections automatically

```python
@with_db_connection
def get_user(conn, user_id):
    # Connection provided and managed automatically
```

3. **@transactional**: Ensures atomic database operations

```python
@transactional
def update_user_email(conn, user_id, email):
    # Automatic rollback on exceptions
```

4. **@retry_on_failure**: Implements retry logic with exponential backoff

```python
@retry_on_failure(retries=3, delay=1)
def unreliable_operation():
    # Automatically retries on failure
```

5. **@cache_query**: Caches query results to improve performance

```python
@cache_query
def expensive_query(query):
    # Results cached for subsequent calls
```

**Learning Outcomes**: Advanced Python decorators, database transaction management, resilience patterns, and performance optimization.

### 🔄 [python-generators-0x00](./python-generators-0x00/)

**Focus**: Memory-Efficient Data Processing

Demonstrates powerful generator patterns for handling large datasets efficiently with minimal memory footprint.

#### Key Features

- 🌊 **Data Streaming**: Process large datasets without loading into memory
- 📦 **Batch Processing**: Efficient batch operations on user data
- 📄 **Lazy Pagination**: Memory-efficient pagination implementation
- 📊 **Stream Analytics**: Real-time data analysis using generators

#### Files

- `seed.py` - Database setup and sample data generation
- `0-stream_users.py` - User streaming generator
- `1-batch_processing.py` - Batch processing with age filtering
- `2-lazy_paginate.py` - Lazy pagination implementation
- `4-stream_ages.py` - Memory-efficient age calculation

#### Example Usage

```python
# Stream users one by one
for user in stream_users():
    process_user(user)  # Memory efficient

# Process in batches
for batch in batch_processing(batch_size=100):
    process_batch(batch)

# Lazy pagination
for page in lazy_paginate(page_size=50):
    display_page(page)
```

**Learning Outcomes**: Generator patterns, memory optimization, lazy evaluation, and efficient data processing techniques.

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7+ (3.13+ recommended)
- pip (Python package installer)
- Git
- Virtual environment tool (venv, conda, etc.)

### Quick Start

1. **Clone the Repository**

```bash
git clone https://github.com/kimoban/alx-backend-python.git
cd alx-backend-python
```

2. **Set Up Virtual Environment**

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

3. **Install Dependencies**

Each sub-project has its own requirements. Install dependencies based on the project you want to explore:

```bash
# For Django projects
cd Django-Middleware-0x03
pip install -r requirements.txt

# For testing projects
cd 0x03-Unittests_and_integration_tests
pip install requests

# For async projects
pip install aiosqlite

# For generator projects
pip install mysql-connector-python
```

### Project-Specific Setup

#### Django Projects Setup

```bash
# Navigate to Django project
cd Django-Middleware-0x03

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

#### Testing Projects Setup

```bash
# Navigate to testing project
cd 0x03-Unittests_and_integration_tests

# Run all tests
python -m unittest discover

# Run specific test files
python -m unittest test_utils.py
python -m unittest test_client.py
```

#### Database Projects Setup

```bash
# For generator projects
cd python-generators-0x00

# Set up database (ensure MySQL is running)
python seed.py

# Run generator examples
python 0-stream_users.py
python 1-batch_processing.py
```

---

## 🧪 Testing

### Running All Tests

```bash
# Unit and Integration Tests
cd 0x03-Unittests_and_integration_tests
python -m unittest discover -v

# Django Tests
cd Django-Middleware-0x03
python manage.py test

# Messaging App Tests
cd messaging_app
python manage.py test
```

### Test Coverage
Each project includes comprehensive test suites:

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow validation
- **Middleware Tests**: Custom middleware functionality
- **API Tests**: RESTful endpoint validation

## 📚 Learning Objectives

This repository demonstrates proficiency in:

### Core Python Concepts

- ✅ **Object-Oriented Programming**: Classes, inheritance, polymorphism
- ✅ **Functional Programming**: Decorators, generators, lambda functions
- ✅ **Async Programming**: asyncio, context managers, concurrent execution
- ✅ **Error Handling**: Exception management, retry patterns
- ✅ **Testing**: Unit tests, integration tests, mocking strategies

### Web Development

- ✅ **Django Framework**: Models, views, middleware, authentication
- ✅ **Django REST Framework**: Serializers, viewsets, permissions
- ✅ **API Design**: RESTful principles, endpoint structure, documentation
- ✅ **Security**: Authentication, authorization, rate limiting
- ✅ **Database Management**: ORM, migrations, query optimization

### Software Engineering Practices

- ✅ **Clean Code**: PEP 8 compliance, readable, maintainable code
- ✅ **Design Patterns**: Decorator, context manager, factory patterns
- ✅ **Performance Optimization**: Memory efficiency, async operations
- ✅ **Error Resilience**: Retry logic, graceful degradation
- ✅ **Documentation**: Comprehensive code documentation

## 🔧 Technologies Used

### Programming Languages

- **Python 3.7+**: Core programming language
- **SQL**: Database queries and management

### Frameworks & Libraries

- **Django 5.2.4**: Web framework for rapid development
- **Django REST Framework 3.16.0**: Powerful toolkit for building APIs
- **asyncio**: Asynchronous programming support
- **unittest**: Python's built-in testing framework
- **requests**: HTTP library for API interactions

### Databases

- **SQLite**: Development database (default)
- **MySQL**: Production database for generators
- **PostgreSQL**: Production-ready database option

### Development Tools

- **Git**: Version control
- **pip**: Package management
- **Virtual Environments**: Isolated development environments

## 📖 Documentation

Each sub-project includes detailed documentation:

- **README files**: Project-specific setup and usage instructions
- **Inline Comments**: Code explanation and context
- **Docstrings**: Function and class documentation
- **API Documentation**: Endpoint specifications and examples

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Make Changes**: Implement your feature or bug fix
4. **Add Tests**: Ensure your changes are properly tested
5. **Commit Changes**: `git commit -m 'Add amazing feature'`
6. **Push to Branch**: `git push origin feature/amazing-feature`
7. **Open Pull Request**: Submit your changes for review

### Code Standards

- Follow PEP 8 style guidelines
- Include comprehensive tests for new features
- Add proper documentation and docstrings
- Ensure backward compatibility

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Author

### Isaiah Kimoban

- GitHub: [@kimoban](https://github.com/kimoban)
- Project: ALX Backend Python Specialization

## 🙏 Acknowledgments

- **ALX Software Engineering Program**: For providing the foundation and structure
- **Django Community**: For excellent documentation and resources
- **Python Community**: For continuous innovation and support
- **Open Source Contributors**: For inspiration and best practices

## 📈 Project Stats

- **Total Projects**: 6 comprehensive sub-projects
- **Languages**: Python, SQL, HTML
- **Frameworks**: Django, Django REST Framework
- **Testing Coverage**: 90%+ across all projects
- **Documentation**: Comprehensive README and inline documentation

<!-- Centered call-to-action (remove HTML for Markdown lint compliance) -->

**🚀 Ready to explore? Start with any sub-project that interests you most!**

[Testing Project](./0x03-Unittests_and_integration_tests/) • [Django Middleware](./Django-Middleware-0x03/) • [Messaging API](./messaging_app/) • [Async Operations](./python-context-async-operations-0x02/) • [Decorators](./python-decorators-0x01/) • [Generators](./python-generators-0x00/)

<!-- End centered call-to-action -->

</p>
