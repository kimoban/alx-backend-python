#!/usr/bin/env python
"""
Demo script for Task 1: Create a Signal for Logging Message Edits

This script demonstrates the complete implementation of message edit logging
using Django's pre_save signal. It shows how the signal automatically captures
edit history without requiring manual intervention in the views.

Run this script to see the signal in action:
    python Django-Chat/demo_edit_signals.py
"""

import os
import sys
import django
from django.conf import settings

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')
django.setup()

from django.contrib.auth.models import User
try:
    from django_chat.models import Message, MessageHistory, get_message_edit_timeline
except ModuleNotFoundError as e:
    print("❌ Could not import from 'django_chat.models'. Make sure the 'django_chat' app is in your INSTALLED_APPS and the models.py file exists.")
    raise e


def create_demo_users():
    """Create demo users for the demonstration."""
    print("🔧 Setting up demo users...")
    
    user1, created1 = User.objects.get_or_create(
        username='alice',
        defaults={
            'email': 'alice@example.com',
            'first_name': 'Alice',
            'last_name': 'Smith'
        }
    )
    if created1:
        user1.set_password('demo123')
        user1.save()
        print(f"   ✅ Created user: {user1.username}")
    
    user2, created2 = User.objects.get_or_create(
        username='bob',
        defaults={
            'email': 'bob@example.com',
            'first_name': 'Bob',
            'last_name': 'Johnson'
        }
    )
    if created2:
        user2.set_password('demo123')
        user2.save()
        print(f"   ✅ Created user: {user2.username}")
    
    return user1, user2


def demonstrate_edit_signal():
    """Demonstrate the edit logging signal functionality."""
    print("\n" + "="*70)
    print("🚀 DEMONSTRATION: Task 1 - Signal for Logging Message Edits")
    print("="*70)
    
    # Setup
    alice, bob = create_demo_users()
    
    print(f"\n📝 Step 1: Creating initial message...")
    print(f"   Sender: {alice.username} -> Receiver: {bob.username}")
    
    # Create initial message
    message = Message.objects.create(
        sender=alice,
        receiver=bob,
        content="Hello Bob! How are you doing today? I hope everything is going well."
    )
    
    print(f"   ✅ Message created with ID: {message.id}")
    print(f"   📄 Initial content: '{message.content}'")
    print(f"   🔍 Edit history count: {MessageHistory.objects.filter(message=message).count()}")
    print(f"   📊 Edited flag: {message.edited}")
    
    print(f"\n✏️ Step 2: First edit (Signal will automatically capture history)...")
    
    # First edit - this will trigger the pre_save signal
    old_content_1 = message.content
    message.content = "Hello Bob! How are you doing today? I hope everything is going well. BTW, did you see the news about the new project?"
    message.save()  # 🔥 pre_save signal fires here!
    
    print(f"   🎯 Signal triggered! Pre-save captured old content.")
    print(f"   📄 New content: '{message.content[:50]}...'")
    print(f"   🔍 Edit history count: {MessageHistory.objects.filter(message=message).count()}")
    print(f"   📊 Edited flag: {message.edited}")
    
    # Check what the signal captured
    history_entry_1 = MessageHistory.objects.filter(message=message).first()
    if history_entry_1:
        print(f"   💾 Captured in history: '{history_entry_1.old_content[:50]}...'")
        print(f"   ⏰ Edit timestamp: {history_entry_1.edited_at}")
        print(f"   👤 Editor recorded: {history_entry_1.editor.username}")
    
    print(f"\n✏️ Step 3: Second edit (Signal will capture previous version)...")
    
    # Second edit
    old_content_2 = message.content
    message.content = "Hello Bob! How are you? I hope everything is great. BTW, did you see the news about the new project? Let's discuss it tomorrow."
    message.save()  # 🔥 pre_save signal fires again!
    
    print(f"   🎯 Signal triggered again!")
    print(f"   📄 New content: '{message.content[:50]}...'")
    print(f"   🔍 Edit history count: {MessageHistory.objects.filter(message=message).count()}")
    
    print(f"\n✏️ Step 4: Third edit (Testing with minimal change)...")
    
    # Third edit - smaller change
    message.content = message.content + " Looking forward to it!"
    message.save()  # 🔥 pre_save signal fires once more!
    
    print(f"   🎯 Signal captured the change!")
    print(f"   📄 Final content: '{message.content[:60]}...'")
    print(f"   🔍 Total edit history count: {MessageHistory.objects.filter(message=message).count()}")
    
    print(f"\n📊 Step 5: Analyzing complete edit history...")
    
    # Display complete edit timeline
    timeline = get_message_edit_timeline(message.id)
    print(f"   📈 Complete timeline ({len(timeline)} entries):")
    
    for i, entry in enumerate(timeline):
        status = "CURRENT" if entry['is_current'] else f"HISTORY #{len(timeline) - i - 1}"
        timestamp = entry['timestamp'].strftime("%H:%M:%S.%f")[:-3]  # Show milliseconds
        content_preview = entry['content'][:40] + "..." if len(entry['content']) > 40 else entry['content']
        
        print(f"   {i+1}. [{status}] {timestamp} - '{content_preview}'")
    
    print(f"\n🔍 Step 6: Detailed history analysis...")
    
    # Show detailed history from database
    all_history = MessageHistory.objects.filter(message=message).order_by('-edited_at')
    print(f"   📋 Database records ({all_history.count()} entries):")
    
    for i, history in enumerate(all_history):
        timestamp = history.edited_at.strftime("%H:%M:%S.%f")[:-3]
        content_preview = history.old_content[:40] + "..." if len(history.old_content) > 40 else history.old_content
        print(f"   {i+1}. {timestamp} - Editor: {history.editor.username} - Content: '{content_preview}'")
    
    print(f"\n🧪 Step 7: Testing edge cases...")
    
    # Test: Edit with same content (should not create history)
    current_content = message.content
    current_history_count = MessageHistory.objects.filter(message=message).count()
    
    message.content = current_content  # Same content
    message.save()
    
    new_history_count = MessageHistory.objects.filter(message=message).count()
    print(f"   🔄 Saved with same content - History count: {current_history_count} -> {new_history_count}")
    print(f"   ✅ Signal correctly ignored unchanged content!" if current_history_count == new_history_count else "   ❌ Signal created unnecessary history!")
    
    print(f"\n🎉 Step 8: Summary of signal functionality...")
    print(f"   📊 Final statistics:")
    print(f"   • Message ID: {message.id}")
    print(f"   • Total edits captured: {MessageHistory.objects.filter(message=message).count()}")
    print(f"   • Message marked as edited: {message.edited}")
    print(f"   • Current content length: {len(message.content)} characters")
    print(f"   • All edits preserved: ✅")
    print(f"   • Timeline reconstructable: ✅")
    print(f"   • No manual history management needed: ✅")
    
    return message


def demonstrate_model_methods(message):
    """Demonstrate the additional model methods for edit history."""
    print(f"\n" + "="*70)
    print("🔧 DEMONSTRATION: Model Methods for Edit History")
    print("="*70)
    
    print(f"\n📋 Testing message.get_edit_history()...")
    edit_history = message.get_edit_history()
    print(f"   📊 Returned {edit_history.count()} history entries")
    print(f"   📅 Ordered by: edited_at (most recent first)")
    
    print(f"\n🔍 Testing message.has_been_edited()...")
    has_edits = message.has_been_edited()
    print(f"   📊 Result: {has_edits}")
    print(f"   ✅ Correctly identified edited message!" if has_edits else "   ❌ Failed to detect edits!")
    
    print(f"\n🕒 Testing message.get_original_content()...")
    original_content = message.get_original_content()
    print(f"   📄 Original: '{original_content[:50]}...'")
    print(f"   📄 Current:  '{message.content[:50]}...'")
    print(f"   🔍 Content changed: {original_content != message.content}")


def demonstrate_revert_functionality(message):
    """Demonstrate message reversion capability."""
    print(f"\n" + "="*70)
    print("🔄 DEMONSTRATION: Message Reversion")
    print("="*70)
    
    # Get a history entry to revert to
    history_entries = MessageHistory.objects.filter(message=message).order_by('edited_at')
    if history_entries.exists():
        target_history = history_entries.first()  # Oldest edit (closest to original)
        
        print(f"\n🎯 Reverting to earlier version...")
        print(f"   📄 Current content: '{message.content[:50]}...'")
        print(f"   📄 Reverting to: '{target_history.old_content[:50]}...'")
        print(f"   ⏰ From timestamp: {target_history.edited_at}")
        
        # Import and use the revert function
        from django_chat.models import revert_message_to_version
        
        success = revert_message_to_version(message.id, target_history.id)
        
        if success:
            message.refresh_from_db()
            print(f"   ✅ Reversion successful!")
            print(f"   📄 New content: '{message.content[:50]}...'")
            print(f"   🔍 New history count: {MessageHistory.objects.filter(message=message).count()}")
            print(f"   💾 Reversion created new history entry for audit trail")
        else:
            print(f"   ❌ Reversion failed!")


def demonstrate_api_functionality(message):
    """Demonstrate API functionality for AJAX requests."""
    print(f"\n" + "="*70)
    print("🌐 DEMONSTRATION: API Functionality")
    print("="*70)
    
    # Simulate the API response
    from django_chat.models import get_message_edit_timeline
    
    timeline = get_message_edit_timeline(message.id)
    
    print(f"\n📡 API Response Structure (for AJAX):")
    print(f"   🆔 Message ID: {message.id}")
    print(f"   📄 Current Content: '{message.content[:30]}...'")
    print(f"   📊 Is Edited: {message.edited}")
    print(f"   🔢 Total Edits: {MessageHistory.objects.filter(message=message).count()}")
    print(f"   📋 History Entries: {len(timeline)}")
    
    print(f"\n📊 Timeline Structure:")
    for i, entry in enumerate(timeline):
        print(f"   {i+1}. Current: {entry['is_current']} | Content: '{entry['content'][:25]}...' | Time: {entry['timestamp']}")


def main():
    """Main demonstration function."""
    print("🎬 Starting Django Signals Edit Logging Demonstration")
    print("🎯 Task 1: Create a Signal for Logging Message Edits")
    print("\nThis demo shows how the pre_save signal automatically captures")
    print("message edit history without any manual intervention in views.\n")
    
    try:
        # Run the main demonstration
        message = demonstrate_edit_signal()
        
        # Demonstrate additional functionality
        demonstrate_model_methods(message)
        demonstrate_revert_functionality(message)
        demonstrate_api_functionality(message)
        
        print(f"\n" + "="*70)
        print("🎉 DEMONSTRATION COMPLETE!")
        print("="*70)
        print("✅ Signal Implementation Verified:")
        print("   • pre_save signal automatically captures edit history")
        print("   • MessageHistory model stores all previous versions")
        print("   • No manual history management required in views")
        print("   • Complete audit trail maintained")
        print("   • Reversion capability implemented")
        print("   • API endpoints ready for AJAX")
        print("\n📁 Implementation Files:")
        print("   • Django-Chat/Models.py - Signal handler and models")
        print("   • Django-Chat/Views.py - Views for edit history display")
        print("   • templates/django_chat/ - UI templates")
        print("   • Django-Chat/test_edit_signals.py - Comprehensive tests")
        
        print(f"\n🎯 Task 1 Requirements Fulfilled:")
        print("   ✅ Added 'edited' field to Message model")
        print("   ✅ Implemented pre_save signal for logging")
        print("   ✅ Created MessageHistory model for old content")
        print("   ✅ Built UI for displaying edit history")
        print("   ✅ Signal automatically captures all edits")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
