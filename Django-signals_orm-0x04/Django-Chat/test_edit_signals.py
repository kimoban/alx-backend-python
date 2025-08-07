"""
Test file for Django-Chat Models - Demonstrates Task 1: Create a Signal for Logging Message Edits

This test file thoroughly tests the message edit logging functionality implemented
using Django's pre_save signal in the Django-Chat/Models.py file.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.signals import pre_save
from django.test.utils import override_settings
import time
from .Models import Message, MessageHistory, log_message_edit


class MessageEditSignalTestCase(TestCase):
    """
    Test case for the message edit logging signal.
    Tests all aspects of Task 1: Create a Signal for Logging Message Edits
    """
    
    def setUp(self):
        """Set up test users and initial data."""
        self.user1 = User.objects.create_user(
            username='sender',
            email='sender@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='receiver',
            email='receiver@test.com',
            password='testpass123'
        )

    def test_message_creation_does_not_trigger_edit_signal(self):
        """Test that creating a new message does not create edit history."""
        # Create a new message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="This is a new message."
        )
        
        # Verify no edit history was created for a new message
        self.assertEqual(MessageHistory.objects.filter(message=message).count(), 0)
        self.assertFalse(message.edited)
        
    def test_message_edit_triggers_signal_and_logs_history(self):
        """Test that editing a message triggers the pre_save signal and logs edit history."""
        # Create initial message
        original_content = "This is the original content."
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content=original_content
        )
        
        # Verify no history exists initially
        self.assertEqual(MessageHistory.objects.filter(message=message).count(), 0)
        self.assertFalse(message.edited)
        
        # Edit the message - this should trigger the pre_save signal
        new_content = "This is the edited content."
        message.content = new_content
        message.save()
        
        # Verify edit history was created by the signal
        history_entries = MessageHistory.objects.filter(message=message)
        self.assertEqual(history_entries.count(), 1)
        
        # Verify the history contains the old content
        history = history_entries.first()
        self.assertEqual(history.old_content, original_content)
        self.assertEqual(history.editor, self.user1)  # Set to sender in our signal
        self.assertIsNotNone(history.edited_at)
        
        # Verify the message is marked as edited
        message.refresh_from_db()
        self.assertTrue(message.edited)
        self.assertEqual(message.content, new_content)

    def test_multiple_edits_create_multiple_history_entries(self):
        """Test that multiple edits create multiple history entries in correct order."""
        # Create initial message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Version 1"
        )
        
        # First edit
        message.content = "Version 2"
        message.save()
        
        # Small delay to ensure different timestamps
        time.sleep(0.01)
        
        # Second edit
        message.content = "Version 3"
        message.save()
        
        # Verify two history entries were created
        history_entries = MessageHistory.objects.filter(message=message).order_by('edited_at')
        self.assertEqual(history_entries.count(), 2)
        
        # Verify the history contains the correct old content in order
        self.assertEqual(history_entries[0].old_content, "Version 1")  # First edit saved original
        self.assertEqual(history_entries[1].old_content, "Version 2")  # Second edit saved first edit
        
        # Verify current message content
        self.assertEqual(message.content, "Version 3")
        self.assertTrue(message.edited)

    def test_edit_with_same_content_does_not_create_history(self):
        """Test that saving a message with unchanged content does not create history."""
        # Create initial message
        original_content = "No change content"
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content=original_content
        )
        
        # "Edit" with same content
        message.content = original_content  # Same content
        message.save()
        
        # Verify no history was created since content didn't change
        self.assertEqual(MessageHistory.objects.filter(message=message).count(), 0)

    def test_message_history_model_methods(self):
        """Test the custom methods added to Message model for edit history."""
        # Create and edit a message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original"
        )
        
        message.content = "Edited once"
        message.save()
        
        message.content = "Edited twice"
        message.save()
        
        # Test get_edit_history method
        history = message.get_edit_history()
        self.assertEqual(history.count(), 2)
        
        # Test has_been_edited method
        self.assertTrue(message.has_been_edited())
        
        # Test get_original_content method
        original = message.get_original_content()
        self.assertEqual(original, "Original")

    def test_signal_handles_nonexistent_message_gracefully(self):
        """Test that the signal handles edge cases gracefully."""
        # Create a message instance without saving to DB first
        message = Message(
            sender=self.user1,
            receiver=self.user2,
            content="Test content"
        )
        
        # This should not raise an exception even though message doesn't exist in DB
        try:
            message.save()  # First save - should not create history
            self.assertEqual(MessageHistory.objects.filter(message=message).count(), 0)
        except Exception as e:
            self.fail(f"Signal raised unexpected exception: {e}")

    def test_edit_history_ordering(self):
        """Test that edit history is properly ordered by timestamp."""
        # Create initial message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Version 1"
        )
        
        # Make several edits with small delays
        for i in range(2, 6):  # Versions 2-5
            time.sleep(0.01)  # Ensure different timestamps
            message.content = f"Version {i}"
            message.save()
        
        # Get history ordered by edited_at (most recent first)
        history = MessageHistory.objects.filter(message=message).order_by('-edited_at')
        
        # Verify ordering - most recent edit should have "Version 4" as old content
        self.assertEqual(history[0].old_content, "Version 4")
        self.assertEqual(history[1].old_content, "Version 3")
        self.assertEqual(history[2].old_content, "Version 2")
        self.assertEqual(history[3].old_content, "Version 1")

    def test_editor_tracking_in_history(self):
        """Test that the editor is properly tracked in edit history."""
        # Create initial message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original content"
        )
        
        # Edit the message
        message.content = "Edited content"
        message.save()
        
        # Verify editor was recorded
        history = MessageHistory.objects.filter(message=message).first()
        self.assertEqual(history.editor, self.user1)

    def test_database_integrity_with_edits(self):
        """Test that database integrity is maintained during edits."""
        # Create message and edit it
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original"
        )
        
        message.content = "Edited"
        message.save()
        
        # Verify foreign key relationships are intact
        history = MessageHistory.objects.filter(message=message).first()
        self.assertEqual(history.message, message)
        self.assertEqual(history.message.sender, self.user1)
        
        # Test cascade deletion
        original_history_count = MessageHistory.objects.count()
        message.delete()
        
        # History should be deleted when message is deleted (CASCADE)
        remaining_history_count = MessageHistory.objects.count()
        self.assertEqual(remaining_history_count, original_history_count - 1)


class MessageEditFunctionalityTestCase(TestCase):
    """
    Test case for the additional functionality supporting edit history display.
    Tests the utility functions and model methods.
    """
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
    def test_get_message_edit_timeline_function(self):
        """Test the get_message_edit_timeline utility function."""
        from .Models import get_message_edit_timeline
        
        # Create and edit a message
        message = Message.objects.create(
            sender=self.user,
            receiver=self.user,
            content="Original timeline content"
        )
        
        message.content = "First edit"
        message.save()
        
        message.content = "Second edit"
        message.save()
        
        # Get timeline
        timeline = get_message_edit_timeline(message.id)
        
        # Should have 3 entries: current + 2 history
        self.assertEqual(len(timeline), 3)
        
        # First entry should be current version
        current_entry = timeline[0]
        self.assertTrue(current_entry['is_current'])
        self.assertEqual(current_entry['content'], "Second edit")
        
        # Verify historical entries
        self.assertEqual(timeline[1]['content'], "First edit")
        self.assertEqual(timeline[2]['content'], "Original timeline content")

    def test_revert_message_to_version_function(self):
        """Test the revert_message_to_version utility function."""
        from .Models import revert_message_to_version
        
        # Create and edit a message
        message = Message.objects.create(
            sender=self.user,
            receiver=self.user,
            content="Original"
        )
        
        message.content = "First edit"
        message.save()
        
        message.content = "Second edit"
        message.save()
        
        # Get a history entry to revert to
        history_entry = MessageHistory.objects.filter(message=message).first()
        
        # Revert to that version
        success = revert_message_to_version(message.id, history_entry.id)
        self.assertTrue(success)
        
        # Verify message was reverted
        message.refresh_from_db()
        self.assertEqual(message.content, history_entry.old_content)
        
        # Verify revert created a new history entry
        self.assertTrue(MessageHistory.objects.filter(message=message, old_content="Second edit").exists())


class SignalIntegrationTestCase(TestCase):
    """
    Integration tests to ensure the signal works properly in various scenarios.
    """
    
    def setUp(self):
        """Set up test data."""
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

    def test_signal_with_bulk_operations(self):
        """Test that signals work correctly with bulk operations."""
        # Create multiple messages
        messages = []
        for i in range(5):
            message = Message.objects.create(
                sender=self.user1,
                receiver=self.user2,
                content=f"Message {i}"
            )
            messages.append(message)
        
        # Edit each message individually (signals should fire)
        for i, message in enumerate(messages):
            message.content = f"Edited Message {i}"
            message.save()
        
        # Verify all edits were logged
        total_history = MessageHistory.objects.count()
        self.assertEqual(total_history, 5)

    def test_signal_with_transaction_rollback(self):
        """Test signal behavior during transaction rollback."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original"
        )
        
        try:
            with transaction.atomic():
                # Edit message (signal should fire)
                message.content = "Edited"
                message.save()
                
                # Force a rollback
                raise Exception("Forced rollback")
        except Exception:
            pass
        
        # After rollback, message should be unchanged
        message.refresh_from_db()
        self.assertEqual(message.content, "Original")
        
        # History should also be rolled back
        self.assertEqual(MessageHistory.objects.filter(message=message).count(), 0)

    def test_concurrent_edits(self):
        """Test signal behavior with concurrent edits."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original"
        )
        
        # Simulate concurrent edits by creating multiple instances
        message1 = Message.objects.get(id=message.id)
        message2 = Message.objects.get(id=message.id)
        
        # Edit both instances
        message1.content = "Edit 1"
        message2.content = "Edit 2"
        
        # Save both (last one wins)
        message1.save()
        message2.save()
        
        # Should have 2 history entries
        history_count = MessageHistory.objects.filter(message=message).count()
        self.assertEqual(history_count, 2)


# Run the tests
if __name__ == '__main__':
    import unittest
    unittest.main()
