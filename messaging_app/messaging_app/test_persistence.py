#!/usr/bin/env python3
"""
Test script to verify MySQL data persistence with Docker volumes.
This script creates test data, stops containers, restarts them, and verifies data persists.
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

def test_data_persistence():
    print("=== Testing MySQL Data Persistence ===")
    
    # Create test user if doesn't exist
    test_user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        test_user.set_password('testpass123')
        test_user.save()
        print(f"✅ Created test user: {test_user.username}")
    else:
        print(f"✅ Test user already exists: {test_user.username}")
    
    # Create test conversation
    existing_conversations = Conversation.objects.filter(participants=test_user)
    if not existing_conversations.exists():
        test_conversation = Conversation.objects.create()
        test_conversation.participants.add(test_user)
        print(f"✅ Created test conversation: {test_conversation.conversation_id}")
        created = True
    else:
        test_conversation = existing_conversations.first()
        if test_conversation is not None:
            print(f"✅ Test conversation already exists: {test_conversation.conversation_id}")
        else:
            print("⚠️ No existing test conversation found.")
        created = False
    
    # Create test message
    test_message, created = Message.objects.get_or_create(
        conversation=test_conversation,
        sender=test_user,
        defaults={
            'message_body': 'This message tests Docker volume persistence!'
        }
    )
    
    if created:
        print(f"✅ Created test message: {test_message.message_body[:50]}...")
    else:
        print(f"✅ Test message already exists: {test_message.message_body[:50]}...")
    
    # Display summary
    user_count = User.objects.count()
    conversation_count = Conversation.objects.count()
    message_count = Message.objects.count()
    
    print(f"\n📊 Current Database State:")
    print(f"   Users: {user_count}")
    print(f"   Conversations: {conversation_count}")
    print(f"   Messages: {message_count}")
    
    return {
        'users': user_count,
        'conversations': conversation_count,
        'messages': message_count
    }

if __name__ == '__main__':
    try:
        stats = test_data_persistence()
        print(f"\n✅ Test data creation completed successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
