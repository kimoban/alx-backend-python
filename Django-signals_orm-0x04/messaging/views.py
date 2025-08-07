from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Prefetch
from .models import Message, MessageHistory, Notification

Message.unread.unread_for_user

cache_page
cache_page, 60

@login_required
def inbox(request):
    """Display user's inbox with unread messages."""
    # Use custom manager to get unread messages with optimizations
    unread_messages = Message.unread.for_user(request.user).only(
        'id', 'sender__username', 'content', 'timestamp', 'parent_message'
    ).select_related('sender', 'parent_message')
    
    # Get read messages as well
    read_messages = Message.objects.filter(
        receiver=request.user, 
        read=True
    ).only(
        'id', 'sender__username', 'content', 'timestamp', 'parent_message'
    ).select_related('sender', 'parent_message')[:20]  # Limit to recent 20
    
    context = {
        'unread_messages': unread_messages,
        'read_messages': read_messages,
        'unread_count': Message.unread.unread_count(request.user),
    }
    
    return render(request, 'messaging/inbox.html', context)


@login_required
def send_message(request):
    """Send a new message."""
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        parent_message_id = request.POST.get('parent_message_id')
        
        try:
            receiver = User.objects.get(id=receiver_id)
            
            message_data = {
                'sender': request.user,
                'receiver': receiver,
                'content': content,
            }
            
            # Add parent message if this is a reply
            if parent_message_id:
                parent_message = get_object_or_404(Message, id=parent_message_id)
                message_data['parent_message'] = parent_message
            
            message = Message.objects.create(**message_data)
            
            messages.success(request, 'Message sent successfully!')
            return redirect('messaging:inbox')
            
        except User.DoesNotExist:
            messages.error(request, 'Receiver not found.')
    
    # Get all users except current user for receiver selection
    users = User.objects.exclude(id=request.user.id)
    
    return render(request, 'messaging/send_message.html', {'users': users})


@login_required
def message_detail(request, message_id):
    """Display message details with thread and edit history."""
    message = get_object_or_404(Message, id=message_id)
    
    # Check if user has permission to view this message
    if message.sender != request.user and message.receiver != request.user:
        messages.error(request, 'You do not have permission to view this message.')
        return redirect('messaging:inbox')
    
    # Mark as read if user is the receiver
    if message.receiver == request.user and not message.read:
        message.read = True
        message.save(update_fields=['read'])
    
    # Get thread messages with optimized queries
    thread_messages = message.get_thread_messages().prefetch_related(
        Prefetch('edit_history', queryset=MessageHistory.objects.order_by('-edited_at'))
    )
    
    # Get edit history for this specific message
    edit_history = MessageHistory.objects.filter(message=message).order_by('-edited_at')
    
    context = {
        'message': message,
        'thread_messages': thread_messages,
        'edit_history': edit_history,
    }
    
    return render(request, 'messaging/message_detail.html', context)


@login_required
def edit_message(request, message_id):
    """Edit a message (only sender can edit)."""
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    
    if request.method == 'POST':
        new_content = request.POST.get('content')
        if new_content and new_content.strip():
            message.content = new_content.strip()
            message.save()
            messages.success(request, 'Message updated successfully!')
            return redirect('messaging:message_detail', message_id=message.pk)
        else:
            messages.error(request, 'Message content cannot be empty.')
    
    return render(request, 'messaging/edit_message.html', {'message': message})


@login_required
def notifications(request):
    """Display user notifications."""
    user_notifications = Notification.objects.filter(
        user=request.user
    ).select_related('message', 'message__sender').order_by('-created_at')
    
    # Mark notifications as read when viewed
    unread_notifications = user_notifications.filter(read=False)
    unread_notifications.update(read=True)
    
    context = {
        'notifications': user_notifications[:50],  # Limit to recent 50
    }
    
    return render(request, 'messaging/notifications.html', context)


@login_required
def delete_user_account(request):
    """
    Delete user account and all related data.
    This handles Task 2: Use Signals for Deleting User-Related Data
    """
    if request.method == 'POST':
        confirm = request.POST.get('confirm')
        if confirm == 'DELETE':
            user = request.user
            username = user.username
            
            # Log out the user first
            from django.contrib.auth import logout
            logout(request)
            
            # Delete the user (signals will handle cleanup)
            user.delete()
            
            messages.success(request, f'Account {username} has been successfully deleted.')
            return redirect('home')  # Redirect to a home page or login
        else:
            messages.error(request, 'Please type "DELETE" to confirm account deletion.')
    
    return render(request, 'messaging/delete_account.html')


def api_unread_count(request):
    """API endpoint to get unread message count."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    count = Message.unread.unread_count(request.user)
    return JsonResponse({'unread_count': count})
