from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Message(models.Model):
    """Model representing a message between users with edit tracking."""
    
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
    edited = models.BooleanField(default=False)  # Track if message has been edited
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    
    class Meta:
        ordering = ['-timestamp']
        db_table = 'django_chat_message'
    
    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:50]}..."
    
    def get_edit_history(self):
        """Get all edit history for this message ordered by most recent first."""
        return self.messagehistory_set.all().order_by('-edited_at')
    
    def has_been_edited(self):
        """Check if this message has been edited."""
        return self.edited or self.messagehistory_set.exists()
    
    def get_original_content(self):
        """Get the original content of the message."""
        oldest_history = self.messagehistory_set.order_by('edited_at').first()
        return oldest_history.old_content if oldest_history else self.content


class MessageHistory(models.Model):
    """Model to store edit history of messages."""
    
    message = models.ForeignKey(
        'Message', 
        on_delete=models.CASCADE, 
        related_name='edit_history'
    )
    old_content = models.TextField(
        help_text="The previous content of the message before it was edited"
    )
    edited_at = models.DateTimeField(default=timezone.now)
    editor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User who made the edit"
    )
    
    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = "Message histories"
        db_table = 'django_chat_message_history'
    
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
        db_table = 'django_chat_notification'
    
    def __str__(self):
        return f"Notification for {self.user}: {self.content[:50]}..."


# Signal handler for logging message edits
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal to log message edits before saving.
    This implements Task 1: Create a Signal for Logging Message Edits
    
    The signal:
    1. Captures the old content before the message is updated
    2. Creates a MessageHistory record with the old content
    3. Marks the message as edited
    4. Stores who made the edit
    """
    if instance.pk:  # Only for existing messages (updates, not new creations)
        try:
            # Get the original message from database
            original_message = Message.objects.get(pk=instance.pk)
            
            # Check if content has actually changed
            if original_message.content != instance.content:
                # Create history record with old content
                MessageHistory.objects.create(
                    message=original_message,
                    old_content=original_message.content,
                    # Note: In a real application, you'd get the editor from the request
                    # For this demo, we'll use the sender
                    editor=original_message.sender
                )
                
                # Mark the message as edited
                instance.edited = True
                
                print(f"[SIGNAL] Message {instance.pk} edited. Old content saved to history.")
                
        except Message.DoesNotExist:
            # This is a new message, not an edit
            pass


# Additional utility functions for edit history
def get_message_edit_timeline(message_id):
    """
    Get a complete timeline of edits for a message.
    Returns a list of dictionaries with edit information.
    """
    try:
        message = Message.objects.get(id=message_id)
        timeline = []
        
        # Add current version
        timeline.append({
            'content': message.content,
            'timestamp': message.timestamp,
            'is_current': True,
            'edited_at': None,
            'editor': message.sender,
        })
        
        # Add edit history
        for history in message.get_edit_history():
            timeline.append({
                'content': history.old_content,
                'timestamp': history.edited_at,
                'is_current': False,
                'edited_at': history.edited_at,
                'editor': history.editor,
            })
        
        return timeline
        
    except Message.DoesNotExist:
        return []


def revert_message_to_version(message_id, history_id):
    """
    Revert a message to a previous version from its edit history.
    This creates a new edit entry and updates the current content.
    """
    try:
        message = Message.objects.get(id=message_id)
        history_entry = MessageHistory.objects.get(id=history_id, message=message)
        
        # Save current content to history before reverting
        MessageHistory.objects.create(
            message=message,
            old_content=message.content,
            editor=message.sender  # In real app, get from request
        )
        
        # Revert to old content
        message.content = history_entry.old_content
        message.edited = True
        message.save()
        
        return True
        
    except (Message.DoesNotExist, MessageHistory.DoesNotExist):
        return False
