from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

edited_by

class UnreadMessagesManager(models.Manager):
    """Custom manager for filtering unread messages for a specific user."""
    
    def for_user(self, user):
        """Get all unread messages for a specific user."""
        return self.get_queryset().filter(receiver=user, read=False)
    
    def unread_count(self, user):
        """Get count of unread messages for a user."""
        return self.for_user(user).count()


class Message(models.Model):
    """Model representing a message between users."""
    
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    
    # Default manager
    objects = models.Manager()
    
    # Custom manager for unread messages
    unread = UnreadMessagesManager()
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:50]}..."
    
    def get_replies(self):
        """Get all replies to this message recursively."""
        return Message.objects.filter(parent_message=self).select_related(
            'sender', 'receiver'
        ).prefetch_related('replies')
    
    def is_thread_starter(self):
        """Check if this message starts a thread."""
        return self.parent_message is None
    
    def get_thread_messages(self):
        """Get all messages in the thread including this one and all replies."""
        if self.is_thread_starter():
            return Message.objects.filter(
                models.Q(id=self.id) | models.Q(parent_message=self)
            ).select_related('sender', 'receiver').order_by('timestamp')
        else:
            # If this is a reply, get the thread starter and all its replies
            thread_starter = self.parent_message
            return Message.objects.filter(
                models.Q(id=thread_starter.id) | models.Q(parent_message=thread_starter)
            ).select_related('sender', 'receiver').order_by('timestamp')


class MessageHistory(models.Model):
    """Model to store edit history of messages."""
    
    message = models.ForeignKey(
        Message, 
        on_delete=models.CASCADE, 
        related_name='edit_history'
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = "Message histories"
    
    def __str__(self):
        return f"Edit history for message {self.message.id} at {self.edited_at}"


class Notification(models.Model):
    """Model for user notifications."""
    
    NOTIFICATION_TYPES = [
        ('message', 'New Message'),
        ('reply', 'Message Reply'),
        ('edit', 'Message Edited'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    message = models.ForeignKey(
        Message, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES, 
        default='message'
    )
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.user}: {self.content[:50]}..."
