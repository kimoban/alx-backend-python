from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.db.models import Q, Prefetch
from django.utils import timezone
from messaging.models import Message, MessageHistory


@cache_page(60)  # Cache for 60 seconds as specified in Task 5
@login_required
def conversation_list(request, user_id):
    """
    Display cached list of messages in a conversation between current user and specified user.
    This view implements Task 5: Basic view caching with 60 seconds timeout.
    """
    other_user = get_object_or_404(User, id=user_id)
    
    # Get all messages between the two users
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).select_related(
        'sender', 'receiver', 'parent_message'
    ).prefetch_related(
        Prefetch('edit_history', queryset=MessageHistory.objects.order_by('-edited_at')[:3])
    ).order_by('timestamp')
    
    # Get conversation participants
    participants = [request.user, other_user]
    
    # Mark messages as read for current user
    unread_messages = messages.filter(receiver=request.user, read=False)
    unread_messages.update(read=True)
    
    context = {
        'messages': messages,
        'other_user': other_user,
        'participants': participants,
        'total_messages': messages.count(),
    }
    
    return render(request, 'chats/conversation_list.html', context)


@login_required
def conversation_users(request):
    """
    Display list of users the current user has conversations with.
    This view is not cached to show real-time conversation updates.
    """
    # Get users who have sent messages to current user or received messages from current user
    user_ids = set()
    
    # Users who sent messages to current user
    senders = Message.objects.filter(receiver=request.user).values_list('sender_id', flat=True).distinct()
    user_ids.update(senders)
    
    # Users who received messages from current user
    receivers = Message.objects.filter(sender=request.user).values_list('receiver_id', flat=True).distinct()
    user_ids.update(receivers)
    
    # Remove current user from the list
    user_ids.discard(request.user.id)
    
    # Get user objects with latest message info
    conversation_users = []
    for user_id in user_ids:
        user = User.objects.get(id=user_id)
        
        # Get the latest message between users
        latest_message = Message.objects.filter(
            Q(sender=request.user, receiver=user) |
            Q(sender=user, receiver=request.user)
        ).order_by('-timestamp').first()
        
        # Get unread count
        unread_count = Message.objects.filter(
            sender=user, receiver=request.user, read=False
        ).count()
        
        conversation_users.append({
            'user': user,
            'latest_message': latest_message,
            'unread_count': unread_count,
        })
    
    # Sort by latest message timestamp
    conversation_users.sort(
        key=lambda x: x['latest_message'].timestamp if x['latest_message'] else timezone.now(),
        reverse=True
    )
    
    context = {
        'conversation_users': conversation_users,
    }
    
    return render(request, 'chats/conversation_users.html', context)


@cache_page(30)  # Cache for 30 seconds
def public_chat_stats(request):
    """
    Display public chat statistics.
    This is an example of another cached view with different timeout.
    """
    from django.db.models import Count
    from django.utils import timezone
    from datetime import timedelta
    
    # Get statistics
    total_messages = Message.objects.count()
    total_users = User.objects.count()
    
    # Messages in last 24 hours
    yesterday = timezone.now() - timedelta(days=1)
    recent_messages = Message.objects.filter(timestamp__gte=yesterday).count()
    
    # Most active users (by message count)
    active_users = User.objects.annotate(
        message_count=Count('sent_messages')
    ).order_by('-message_count')[:5]
    
    # Recent conversations
    recent_conversations = Message.objects.select_related(
        'sender', 'receiver'
    ).order_by('-timestamp')[:10]
    
    context = {
        'total_messages': total_messages,
        'total_users': total_users,
        'recent_messages': recent_messages,
        'active_users': active_users,
        'recent_conversations': recent_conversations,
        'cache_info': {
            'cached_at': timezone.now(),
            'cache_timeout': 30,
        }
    }
    
    return render(request, 'chats/public_stats.html', context)
