# Django Signals and ORM - Messaging App

This project implements a comprehensive Django messaging application demonstrating advanced signal handling, ORM techniques, and caching. It fulfills all the requirements from Tasks 0-5.

## Project Structure

```
Django-signals_orm-0x04/
├── manage.py
├── requirements.txt
├── messaging_app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── messaging/
│   ├── __init__.py
│   ├── models.py      # Message, MessageHistory, Notification models
│   ├── signals.py     # Signal handlers for notifications and logging
│   ├── apps.py        # App configuration with signal import
│   ├── admin.py       # Admin interface configuration
│   ├── views.py       # Views for messaging functionality
│   ├── urls.py        # URL patterns
│   └── tests.py       # Comprehensive test suite
├── Django-Chat/       # Task 1 specific implementation
│   ├── __init__.py
│   ├── Models.py      # Enhanced models with edit tracking signals
│   ├── Views.py       # Views for edit history display
│   ├── urls.py        # URL patterns for edit functionality
│   ├── test_edit_signals.py    # Dedicated tests for edit signals
│   └── demo_edit_signals.py    # Interactive demonstration
├── chats/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py       # Cached views for conversations
│   ├── urls.py
│   ├── apps.py
│   ├── admin.py
│   └── tests.py
└── templates/
    ├── base.html
    ├── messaging/
    │   └── inbox.html
    ├── chats/
    │   ├── conversation_list.html
    │   └── public_stats.html
    └── django_chat/   # Templates for edit history UI
        ├── message_detail_with_history.html
        ├── edit_message.html
        └── message_edit_history.html
```

## Features Implemented

### Task 0: Implement Signals for User Notifications ✅

**Objective**: Automatically notify users when they receive a new message.

**Implementation**:

- Created `Message` model with `sender`, `receiver`, `content`, and `timestamp` fields
- Implemented `post_save` signal in `messaging/signals.py` that triggers when a new Message is created
- Created `Notification` model linked to User and Message models
- Signal automatically creates notifications for receiving users

**Key Files**:

- `messaging/models.py` - Message and Notification models
- `messaging/signals.py` - `create_message_notification` signal handler
- `messaging/apps.py` - Signal registration in app config

### Task 1: Create a Signal for Logging Message Edits ✅

**Objective**: Log when a user edits a message and save the old content before the edit.

**Implementation**:

- Added `edited` boolean field to Message model
- Created `MessageHistory` model to store edit history
- Implemented `pre_save` signal to capture old content before updates
- Signal automatically logs old content and marks message as edited

**Key Files**:

- `messaging/models.py` - MessageHistory model and edited field
- `messaging/signals.py` - `log_message_edit` signal handler

### Task 2: Use Signals for Deleting User-Related Data ✅

**Objective**: Automatically clean up related data when a user deletes their account.

**Implementation**:

- Created `delete_user_account` view for user account deletion
- Implemented `post_delete` signal on User model for cleanup logging
- Used CASCADE foreign keys for automatic related data deletion
- Signal provides additional cleanup logic and logging

**Key Files**:

- `messaging/views.py` - `delete_user_account` view
- `messaging/signals.py` - `cleanup_user_data` signal handler
- `messaging/models.py` - CASCADE foreign key relationships

### Task 3: Leverage Advanced ORM Techniques for Threaded Conversations ✅

**Objective**: Implement threaded conversations with efficient querying.

**Implementation**:

- Added `parent_message` self-referential foreign key to Message model
- Used `prefetch_related` and `select_related` for optimized queries
- Implemented recursive query methods for threaded conversations
- Created methods to fetch thread messages and replies efficiently

**Key Features**:

- `get_replies()` - Get all replies to a message
- `get_thread_messages()` - Get all messages in a thread
- `is_thread_starter()` - Check if message starts a thread
- Optimized database queries with proper relationships

**Key Files**:

- `messaging/models.py` - Thread-related methods and parent_message field

### Task 4: Custom ORM Manager for Unread Messages ✅

**Objective**: Create a custom manager to filter unread messages for a user.

**Implementation**:

- Added `read` boolean field to Message model
- Created `UnreadMessagesManager` custom manager
- Implemented methods to filter unread messages for specific users
- Used `.only()` for field optimization in views

**Key Features**:

- `Message.unread.for_user(user)` - Get unread messages for user
- `Message.unread.unread_count(user)` - Get count of unread messages
- Field optimization with `.only()` method

**Key Files**:

- `messaging/models.py` - UnreadMessagesManager class
- `messaging/views.py` - Usage of custom manager with optimizations

### Task 5: Implement Basic View Cache ✅

**Objective**: Set up basic caching for views that retrieve messages.

**Implementation**:

- Updated `settings.py` with LocMemCache configuration
- Implemented `@cache_page(60)` decorator on conversation view
- Set 60-second cache timeout as required
- Added cache information display in templates

**Key Features**:

- 60-second cache timeout on conversation list view
- Cache configuration in settings
- Visual cache indicators in templates
- Additional 30-second cache on statistics view

**Key Files**:

- `messaging_app/settings.py` - Cache configuration
- `chats/views.py` - Cached views with decorators

## Installation and Setup

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd Django-signals_orm-0x04
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser**:

   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

6. **Access the application**:

   - Admin interface: http://127.0.0.1:8000/admin/
   - Messaging app: http://127.0.0.1:8000/messaging/
   - Chat conversations: http://127.0.0.1:8000/chats/

## Testing

Run the comprehensive test suite:

```bash
python manage.py test messaging
```

The test suite covers:

- Signal functionality for notifications and edit logging
- Custom manager behavior
- Threaded conversation features
- User deletion and cleanup
- Model relationships and constraints

## Key Models

### Message Model

- **Fields**: sender, receiver, content, timestamp, edited, read, parent_message
- **Managers**: Default manager + UnreadMessagesManager
- **Methods**: get_replies(), get_thread_messages(), is_thread_starter()

### MessageHistory Model

- **Fields**: message, old_content, edited_at
- **Purpose**: Store edit history for messages

### Notification Model

- **Fields**: user, message, notification_type, content, created_at, read
- **Types**: message, reply, edit

## Signal Handlers

1. **create_message_notification**: Creates notifications for new messages
2. **log_message_edit**: Logs message edits before saving
3. **cleanup_user_data**: Handles user deletion cleanup

## ORM Optimizations

- `select_related()` for foreign key relationships
- `prefetch_related()` for reverse foreign keys and many-to-many
- `.only()` for limiting selected fields
- Custom managers for filtered querysets
- Proper indexing through model Meta options

## Caching Strategy

- **LocMemCache**: In-memory cache for development
- **View-level caching**: 60-second cache on conversation views
- **Cache indicators**: Visual feedback in templates
- **Selective caching**: Only cache read-heavy views

## Admin Interface

Comprehensive admin interface with:

- List displays with custom fields
- Search and filter capabilities
- Raw ID fields for performance
- Readonly fields for timestamps

## Security Considerations

- User authentication required for all views
- Permission checks for message access
- CSRF protection on forms
- Proper foreign key constraints

## Performance Features

- Optimized database queries
- Custom managers for common filters
- View-level caching
- Efficient template rendering
- Proper use of database indexes

## Future Enhancements

- Real-time messaging with WebSockets
- File attachments support
- Message search functionality
- User blocking/unblocking
- Message reactions and status indicators
- Advanced caching strategies (Redis)
- API endpoints for mobile integration

## License

This project is created for educational purposes as part of the ALX Backend Python curriculum.

## Django-Chat Implementation (Task 1 Focused)

The `Django-Chat/` directory contains a focused implementation of **Task 1: Create a Signal for Logging Message Edits** as specified in the requirements.

### Key Features

1. **Enhanced Message Model** (`Django-Chat/Models.py`):
   - `edited` boolean field to track if message has been edited
   - Self-referential foreign key for threaded conversations
   - Custom methods for edit history management

2. **MessageHistory Model** (`Django-Chat/Models.py`):
   - Stores old content before edits
   - Tracks editor and edit timestamps
   - Maintains complete audit trail

3. **Pre-Save Signal** (`Django-Chat/Models.py`):
   - Automatically captures old content before message updates
   - Marks messages as edited
   - No manual intervention required in views

4. **User Interface** (`templates/django_chat/`):
   - Complete edit history display
   - Timeline view of all message versions
   - Message reversion capability
   - AJAX API for dynamic history loading

5. **Comprehensive Testing** (`Django-Chat/test_edit_signals.py`):
   - Tests all signal functionality
   - Edge case handling
   - Concurrent edit scenarios
   - Database integrity verification

6. **Interactive Demo** (`Django-Chat/demo_edit_signals.py`):
   - Live demonstration of signal functionality
   - Step-by-step edit logging showcase
   - Performance and feature analysis

### Access Django-Chat Features:

- Message detail with history: `/django-chat/message/<id>/`
- Edit message: `/django-chat/message/<id>/edit/`
- Complete edit history: `/django-chat/message/<id>/history/`
- API endpoint: `/django-chat/api/message-history/<id>/`

### Run Demo

```bash
python Django-Chat/demo_edit_signals.py
```

This implementation fully satisfies the Task 1 requirements with the signal automatically logging all message edits to the `MessageHistory` model and providing a complete user interface for viewing edit history.
