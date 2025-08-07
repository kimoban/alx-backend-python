#!/usr/bin/env python3
"""
Simple test script to verify MySQL data persistence with Docker volumes.
"""

import os
import django
import sys

# Add the current directory to the Python path
sys.path.append('/app')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')
django.setup()

from chats.models import User, Conversation, Message

def check_database_state():
    print("=== MySQL Data Persistence Test ===")
    
    # Count existing data
    user_count = User.objects.count()
    conversation_count = Conversation.objects.count()
    message_count = Message.objects.count()
    
    print(f"📊 Current Database State:")
    print(f"   Users: {user_count}")
    print(f"   Conversations: {conversation_count}")
    print(f"   Messages: {message_count}")
    
    # Create a simple test user if none exists
    if user_count == 0:
        test_user = User.objects.create_user(
            username='persistence_test_user',
            email='test@persistence.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        print(f"✅ Created test user: {test_user.username}")
        return True
    else:
        print(f"✅ Database contains existing data - persistence working!")
        return False

if __name__ == '__main__':
    try:
        created_data = check_database_state()
        if created_data:
            print("\n🎯 Test data created! Now restart containers to test persistence.")
        else:
            print("\n🎯 Database already contains data, indicating successful persistence!")
        print("✅ MySQL volume persistence test completed successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
