from django.test import TestCase
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from .models import Message, MessageHistory, Notification
from .signals import create_message_notification, log_message_edit, cleanup_user_data


class MessageSignalsTestCase(TestCase):
    """Test case for message-related signals."""
    
    def setUp(self):
        """Set up test users."""
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
    
    def test_message_notification_signal(self):
        """Test that notifications are created when messages are sent."""
        # Create a new message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello, this is a test message!"
        )
        
        # Check that a notification was created
        notifications = Notification.objects.filter(user=self.user2, message=message)
        self.assertEqual(notifications.count(), 1)
        
        notification = notifications.first()
        self.assertEqual(notification.notification_type, 'message')
        self.assertIn(self.user1.username, notification.content)
        self.assertIn("sent you a message", notification.content)
    
    def test_reply_notification_signal(self):
        """Test that reply notifications are created correctly."""
        # Create original message
        original_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original message"
        )
        
        # Create a reply
        reply = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="This is a reply",
            parent_message=original_message
        )
        
        # Check that a reply notification was created
        notifications = Notification.objects.filter(user=self.user1, message=reply)
        self.assertEqual(notifications.count(), 1)
        
        notification = notifications.first()
        self.assertEqual(notification.notification_type, 'reply')
        self.assertIn("replied to your message", notification.content)
    
    def test_message_edit_logging(self):
        """Test that message edits are logged correctly."""
        # Create a message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original content"
        )
        
        # Edit the message
        message.content = "Edited content"
        message.save()
        
        # Check that edit history was created
        history_entries = MessageHistory.objects.filter(message=message)
        self.assertEqual(history_entries.count(), 1)
        
        history = history_entries.first()
        self.assertEqual(history.old_content, "Original content")
        
        # Check that the message is marked as edited
        message.refresh_from_db()
        self.assertTrue(message.edited)
    
    def test_user_deletion_cleanup(self):
        """Test that user deletion triggers cleanup signal."""
        # Create some test data
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        
        notification = Notification.objects.create(
            user=self.user2,
            message=message,
            content="Test notification"
        )
        
        # Count initial objects
        initial_messages = Message.objects.count()
        initial_notifications = Notification.objects.count()
        
        # Delete user (this should cascade delete related objects)
        user2_id = self.user2.pk
        self.user2.delete()
        
        # Verify that related objects were deleted due to CASCADE
        remaining_messages = Message.objects.filter(
            Q(sender_id=user2_id) | Q(receiver_id=user2_id)
        ).count()
        remaining_notifications = Notification.objects.filter(user_id=user2_id).count()
        
        self.assertEqual(remaining_messages, 0)
        self.assertEqual(remaining_notifications, 0)


class MessageModelTestCase(TestCase):
    """Test case for Message model and custom manager."""
    
    def setUp(self):
        """Set up test users."""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
    
    def test_unread_messages_manager(self):
        """Test the custom UnreadMessagesManager."""
        # Create messages with different read states
        read_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Read message",
            read=True
        )
        
        unread_message1 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Unread message 1",
            read=False
        )
        
        unread_message2 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Unread message 2",
            read=False
        )
        
        # Test unread manager
        unread_messages = Message.unread.for_user(self.user2)
        self.assertEqual(unread_messages.count(), 2)
        
        unread_count = Message.unread.unread_count(self.user2)
        self.assertEqual(unread_count, 2)
        
        # Verify the correct messages are returned
        unread_ids = list(unread_messages.values_list('pk', flat=True))
        self.assertIn(unread_message1.pk, unread_ids)
        self.assertIn(unread_message2.pk, unread_ids)
        self.assertNotIn(read_message.pk, unread_ids)
    
    def test_threaded_conversations(self):
        """Test threaded conversation functionality."""
        # Create original message
        original_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original message"
        )
        
        # Create replies
        reply1 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="First reply",
            parent_message=original_message
        )
        
        reply2 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Second reply",
            parent_message=original_message
        )
        
        # Test thread methods
        self.assertTrue(original_message.is_thread_starter())
        self.assertFalse(reply1.is_thread_starter())
        
        # Test getting replies
        replies = original_message.get_replies()
        self.assertEqual(replies.count(), 2)
        
        # Test getting thread messages
        thread_messages = original_message.get_thread_messages()
        self.assertEqual(thread_messages.count(), 3)  # Original + 2 replies
        
        # Test from reply perspective
        thread_from_reply = reply1.get_thread_messages()
        self.assertEqual(thread_from_reply.count(), 3)


class NotificationModelTestCase(TestCase):
    """Test case for Notification model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.sender = User.objects.create_user(
            username='sender',
            email='sender@test.com',
            password='testpass123'
        )
        
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.user,
            content="Test message"
        )
    
    def test_notification_creation(self):
        """Test notification creation and string representation."""
        notification = Notification.objects.create(
            user=self.user,
            message=self.message,
            notification_type='message',
            content="Test notification content"
        )
        
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.message, self.message)
        self.assertEqual(notification.notification_type, 'message')
        self.assertFalse(notification.read)
        
        # Test string representation
        str_repr = str(notification)
        self.assertIn(self.user.username, str_repr)
        self.assertIn("Test notification", str_repr)
