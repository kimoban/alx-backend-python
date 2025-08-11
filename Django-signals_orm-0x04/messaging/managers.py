"""
Custom managers for the messaging app.
This file implements Task 4: Custom ORM Manager for Unread Messages.
"""

from django.db import models
from django.db.models import Q, Count, Prefetch
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class UnreadMessagesManager(models.Manager):
    """
    Custom manager for filtering unread messages for a user.
    This implements Task 4: Custom ORM Manager for Unread Messages.
    """
    
    def for_user(self, user):
        """
        Get all unread messages for a specific user.
        Uses .only() optimization to retrieve only necessary fields.
        """
        return self.get_queryset().filter(
            receiver=user, 
            read=False
        ).only(
            'id', 'sender_id', 'content', 'timestamp', 'parent_message_id', 'edited'
        ).select_related('sender', 'parent_message')
    
    def unread_count(self, user):
        """Get count of unread messages for a user."""
        return self.for_user(user).count()
    
    def unread_from_sender(self, user, sender):
        """Get unread messages from a specific sender to a user."""
        return self.for_user(user).filter(sender=sender)
    
    def unread_in_conversation(self, user, other_user):
        """Get unread messages in a conversation between two users."""
        return self.get_queryset().filter(
            Q(sender=other_user, receiver=user, read=False)
        ).only(
            'id', 'content', 'timestamp', 'parent_message_id', 'edited'
        ).select_related('sender', 'parent_message')
    
    def recent_unread(self, user, days=7):
        """Get unread messages from the last N days."""
        cutoff_date = timezone.now() - timedelta(days=days)
        return self.for_user(user).filter(timestamp__gte=cutoff_date)
    
    def unread_with_priority(self, user):
        """
        Get unread messages with priority ordering.
        Direct messages first, then replies, ordered by timestamp.
        """
        return self.for_user(user).annotate(
            is_reply=models.Case(
                models.When(parent_message__isnull=False, then=models.Value(1)),
                default=models.Value(0),
                output_field=models.IntegerField()
            )
        ).order_by('is_reply', '-timestamp')
    
    def mark_as_read_bulk(self, user, message_ids=None):
        """
        Bulk mark messages as read for a user.
        If message_ids is provided, only mark those specific messages.
        """
        queryset = self.for_user(user)
        if message_ids:
            queryset = queryset.filter(id__in=message_ids)
        
        return queryset.update(read=True)
    
    def unread_summary_by_sender(self, user):
        """
        Get a summary of unread messages grouped by sender.
        Returns a queryset with sender info and unread count.
        """
        return self.for_user(user).values(
            'sender__id', 
            'sender__username', 
            'sender__first_name', 
            'sender__last_name'
        ).annotate(
            unread_count=Count('id'),
            latest_message=models.Max('timestamp')
        ).order_by('-latest_message')


class ThreadedMessagesManager(models.Manager):
    """
    Custom manager for handling threaded conversations.
    This supports Task 3: Leverage Advanced ORM Techniques for Threaded Conversations.
    """
    
    def thread_starters(self):
        """Get all messages that start threads (no parent message)."""
        return self.get_queryset().filter(parent_message__isnull=True)
    
    def replies_only(self):
        """Get all messages that are replies (have a parent message)."""
        return self.get_queryset().filter(parent_message__isnull=False)
    
    def get_thread(self, thread_starter_id):
        """
        Get all messages in a thread, starting from the thread starter.
        Uses optimized queries with prefetch_related and select_related.
        """
        return self.get_queryset().filter(
            Q(id=thread_starter_id) | Q(parent_message_id=thread_starter_id)
        ).select_related(
            'sender', 'receiver', 'parent_message'
        ).prefetch_related(
            'replies', 'edit_history', 'notifications'
        ).order_by('timestamp')
    
    def get_conversation_threads(self, user1, user2):
        """
        Get all thread starters between two users.
        Useful for displaying conversation overview.
        """
        return self.thread_starters().filter(
            Q(sender=user1, receiver=user2) | Q(sender=user2, receiver=user1)
        ).select_related('sender', 'receiver').order_by('-timestamp')
    
    def popular_threads(self, limit=10):
        """
        Get the most popular threads (with most replies).
        """
        return self.thread_starters().annotate(
            reply_count=Count('replies')
        ).filter(
            reply_count__gt=0
        ).order_by('-reply_count')[:limit]
    
    def recent_active_threads(self, days=7, limit=20):
        """
        Get recently active threads (threads with recent replies).
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Get thread starters that have recent activity
        active_thread_ids = self.get_queryset().filter(
            parent_message__isnull=False,  # This is a reply
            timestamp__gte=cutoff_date     # Recent reply
        ).values_list('parent_message_id', flat=True).distinct()
        
        return self.thread_starters().filter(
            id__in=active_thread_ids
        ).select_related('sender', 'receiver').order_by('-timestamp')[:limit]


class ConversationManager(models.Manager):
    """
    Custom manager for handling conversations between users.
    """
    
    def between_users(self, user1, user2):
        """Get all messages between two users, ordered by timestamp."""
        return self.get_queryset().filter(
            Q(sender=user1, receiver=user2) | Q(sender=user2, receiver=user1)
        ).select_related('sender', 'receiver', 'parent_message').order_by('timestamp')
    
    def conversation_partners(self, user):
        """
        Get all users who have had conversations with the given user.
        Returns User objects with additional conversation metadata.
        """
        # Get unique user IDs who have sent messages to or received from user
        sent_to_ids = self.get_queryset().filter(
            sender=user
        ).values_list('receiver_id', flat=True).distinct()
        
        received_from_ids = self.get_queryset().filter(
            receiver=user
        ).values_list('sender_id', flat=True).distinct()
        
        # Combine and get unique partner IDs
        partner_ids = set(list(sent_to_ids) + list(received_from_ids))
        partner_ids.discard(user.id)  # Remove self
        
        # Return User objects with conversation metadata
        return User.objects.filter(id__in=partner_ids).annotate(
            last_message_time=models.Max(
                'sent_messages__timestamp',
                filter=Q(
                    Q(sent_messages__receiver=user) | Q(received_messages__sender=user)
                )
            ),
            total_messages=Count(
                'sent_messages',
                filter=Q(
                    Q(sent_messages__receiver=user) | Q(received_messages__sender=user)
                )
            ) + Count(
                'received_messages',
                filter=Q(received_messages__sender=user)
            )
        ).order_by('-last_message_time')
    
    def latest_in_conversation(self, user1, user2):
        """Get the latest message in a conversation between two users."""
        return self.between_users(user1, user2).last()
    
    def conversation_summary(self, user):
        """
        Get conversation summary for a user showing all their conversation partners
        with unread counts and latest message info.
        """
        partners = self.conversation_partners(user)
        summary = []
        
        for partner in partners:
            latest_message = self.latest_in_conversation(user, partner)
            unread_count = self.get_queryset().filter(
                sender=partner, receiver=user, read=False
            ).count()
            
            summary.append({
                'partner': partner,
                'latest_message': latest_message,
                'unread_count': unread_count,
                'last_activity': latest_message.timestamp if latest_message else None
            })
        
        return summary


class MessageHistoryManager(models.Manager):
    """
    Custom manager for MessageHistory model.
    Handles edit history queries efficiently.
    """
    
    def for_message(self, message):
        """Get all edit history for a specific message."""
        return self.get_queryset().filter(
            message=message
        ).select_related('editor').order_by('-edited_at')
    
    def recent_edits(self, days=7):
        """Get all message edits from the last N days."""
        cutoff_date = timezone.now() - timedelta(days=days)
        return self.get_queryset().filter(
            edited_at__gte=cutoff_date
        ).select_related('message', 'editor').order_by('-edited_at')
    
    def edits_by_user(self, user):
        """Get all edits made by a specific user."""
        return self.get_queryset().filter(
            editor=user
        ).select_related('message').order_by('-edited_at')
    
    def most_edited_messages(self, limit=10):
        """Get messages with the most edits."""
        return self.get_queryset().values(
            'message__id', 'message__content', 'message__sender__username'
        ).annotate(
            edit_count=Count('id')
        ).order_by('-edit_count')[:limit]


class NotificationManager(models.Manager):
    """
    Custom manager for Notification model.
    """
    
    def unread_for_user(self, user):
        """Get unread notifications for a user."""
        return self.get_queryset().filter(
            user=user, read=False
        ).select_related('message', 'message__sender').order_by('-created_at')
    
    def mark_as_read_bulk(self, user, notification_ids=None):
        """Bulk mark notifications as read."""
        queryset = self.get_queryset().filter(user=user, read=False)
        if notification_ids:
            queryset = queryset.filter(id__in=notification_ids)
        
        return queryset.update(read=True)
    
    def by_type(self, user, notification_type):
        """Get notifications of a specific type for a user."""
        return self.get_queryset().filter(
            user=user, notification_type=notification_type
        ).select_related('message', 'message__sender').order_by('-created_at')
    
    def recent_notifications(self, user, days=30):
        """Get recent notifications for a user."""
        cutoff_date = timezone.now() - timedelta(days=days)
        return self.get_queryset().filter(
            user=user, created_at__gte=cutoff_date
        ).select_related('message', 'message__sender').order_by('-created_at')


# Example usage functions demonstrating the managers
def get_user_dashboard_data(user):
    """
    Example function showing how to use multiple custom managers
    to get comprehensive dashboard data for a user.
    """
    # Import here to avoid circular imports
    from .models import Message, MessageHistory, Notification
    
    return {
        'unread_count': Message.unread.unread_count(user),
        'recent_unread': Message.unread.recent_unread(user, days=3)[:5],
        'unread_by_sender': Message.unread.unread_summary_by_sender(user)[:5],
        'conversation_partners': Message.conversations.conversation_partners(user)[:10],
        'active_threads': Message.threads.recent_active_threads(days=7, limit=5),
        'recent_edits': MessageHistory.objects.recent_edits(days=7)[:5],
        'unread_notifications': Notification.objects.unread_for_user(user)[:10],
    }


def optimize_message_queries():
    """
    Example function showing how the custom managers optimize database queries.
    This demonstrates the performance benefits of using .only(), select_related(), etc.
    """
    # Import here to avoid circular imports
    from .models import Message
    from django.contrib.auth.models import User
    
    user = User.objects.first()
    
    # Before: This would fetch all fields for all unread messages
    # unread_messages = Message.objects.filter(receiver=user, read=False)
    
    # After: This only fetches necessary fields and optimizes joins
    unread_messages = Message.unread.for_user(user)
    
    # The custom manager automatically:
    # 1. Uses .only() to limit fields
    # 2. Uses .select_related() for foreign keys
    # 3. Provides semantic method names
    # 4. Encapsulates complex query logic
    
    return unread_messages
