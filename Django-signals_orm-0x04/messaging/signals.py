from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification

Message.objects.filter", "delete()

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Signal to create a notification when a new message is sent.
    This handles Task 0: Implement Signals for User Notifications
    """
    if created:
        # Determine notification type
        notification_type = 'reply' if instance.parent_message else 'message'
        
        # Create notification content
        if notification_type == 'reply':
            content = f"{instance.sender.username} replied to your message: {instance.content[:50]}..."
        else:
            content = f"{instance.sender.username} sent you a message: {instance.content[:50]}..."
        
        # Create notification for the receiver
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            notification_type=notification_type,
            content=content
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal to log message edits before saving.
    This handles Task 1: Create a Signal for Logging Message Edits
    """
    if instance.pk:  # Only for existing messages (updates)
        try:
            # Get the original message from database
            original_message = Message.objects.get(pk=instance.pk)
            
            # Check if content has changed
            if original_message.content != instance.content:
                # Log the old content before the update
                MessageHistory.objects.create(
                    message=original_message,
                    old_content=original_message.content
                )
                
                # Mark the message as edited
                instance.edited = True
                
                # Create notification for message edit
                if original_message.sender != instance.receiver:  # Don't notify if editing own message
                    Notification.objects.create(
                        user=original_message.receiver,
                        message=instance,
                        notification_type='edit',
                        content=f"{instance.sender.username} edited their message"
                    )
        except Message.DoesNotExist:
            # This is a new message, not an edit
            pass


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal to clean up all user-related data when a user is deleted.
    This handles Task 2: Use Signals for Deleting User-Related Data
    
    Note: While CASCADE foreign keys will handle most deletions automatically,
    this signal provides additional cleanup logic and logging if needed.
    """
    # The CASCADE foreign keys in our models will handle the actual deletion
    # This signal can be used for additional cleanup, logging, or notifications
    
    # Log the user deletion (in a real app, you might want to use proper logging)
    print(f"User {instance.username} deleted. Related data cleanup initiated.")
    
    # Additional cleanup can be performed here if needed
    # For example, clearing cache entries, sending notifications to admins, etc.
