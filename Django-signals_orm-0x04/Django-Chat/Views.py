from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Prefetch
from .Models import Message, MessageHistory, Notification, get_message_edit_timeline, revert_message_to_version


@login_required
def message_detail_with_history(request, message_id):
    """
    Display message details with complete edit history.
    This view demonstrates Task 1: Display message edit history in the user interface.
    """
    message = get_object_or_404(Message, id=message_id)
    
    # Check if user has permission to view this message
    if message.sender != request.user and message.receiver != request.user:
        messages.error(request, 'You do not have permission to view this message.')
        return redirect('django_chat:message_list')
    
    # Mark as read if user is the receiver
    if message.receiver == request.user and not message.read:
        message.read = True
        message.save(update_fields=['read'])
    
    # Get complete edit timeline
    edit_timeline = get_message_edit_timeline(message_id)
    
    # Get edit history with related data
    edit_history = MessageHistory.objects.filter(
        message=message
    ).select_related('editor').order_by('-edited_at')
    
    context = {
        'message': message,
        'edit_timeline': edit_timeline,
        'edit_history': edit_history,
        'can_edit': message.sender == request.user,
        'has_edit_history': edit_history.exists(),
    }
    
    return render(request, 'django_chat/message_detail_with_history.html', context)


@login_required
def edit_message_with_history(request, message_id):
    """
    Edit a message and automatically log the edit through signals.
    This demonstrates how the pre_save signal captures edit history.
    """
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    
    if request.method == 'POST':
        new_content = request.POST.get('content', '').strip()
        
        if not new_content:
            messages.error(request, 'Message content cannot be empty.')
            return render(request, 'django_chat/edit_message.html', {'message': message})
        
        if new_content == message.content:
            messages.info(request, 'No changes were made to the message.')
            return redirect('django_chat:message_detail_with_history', message_id=message.id)
        
        # Store old content for comparison (the signal will handle logging)
        old_content = message.content
        
        # Update the message - this will trigger the pre_save signal
        message.content = new_content
        message.save()
        
        messages.success(
            request, 
            f'Message updated successfully! Previous version: "{old_content[:50]}..." has been saved to history.'
        )
        return redirect('django_chat:message_detail_with_history', message_id=message.id)
    
    edit_history_count = MessageHistory.objects.filter(message=message).count()
    context = {
        'message': message,
        'edit_history_count': edit_history_count,
    }
    
    return render(request, 'django_chat/edit_message.html', context)


@login_required
def message_edit_history(request, message_id):
    """
    Display the complete edit history for a message.
    Shows all previous versions with timestamps and editors.
    """
    message = get_object_or_404(Message, id=message_id)
    
    # Check permissions
    if message.sender != request.user and message.receiver != request.user:
        messages.error(request, 'You do not have permission to view this message history.')
        return redirect('django_chat:message_list')
    
    # Get edit history with editor information
    edit_history = MessageHistory.objects.filter(
        message=message
    ).select_related('editor').order_by('-edited_at')
    
    # Get timeline for better visualization
    timeline = get_message_edit_timeline(message_id)
    
    context = {
        'message': message,
        'edit_history': edit_history,
        'timeline': timeline,
        'total_edits': edit_history.count(),
    }
    
    return render(request, 'django_chat/message_edit_history.html', context)


@login_required
def revert_message(request, message_id, history_id):
    """
    Revert a message to a previous version from its edit history.
    Only the message sender can revert their messages.
    """
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    
    if request.method == 'POST':
        success = revert_message_to_version(message_id, history_id)
        
        if success:
            messages.success(request, 'Message has been reverted to the selected version.')
        else:
            messages.error(request, 'Failed to revert message. Please try again.')
    
    return redirect('django_chat:message_detail_with_history', message_id=message_id)


@login_required
def messages_with_edits(request):
    """
    Display all messages that have been edited, with edit counts.
    Useful for seeing which messages have edit history.
    """
    edited_messages = Message.objects.filter(
        Q(edited=True) | Q(messagehistory__isnull=False)
    ).filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).distinct().select_related(
        'sender', 'receiver'
    ).prefetch_related(
        'messagehistory_set'
    ).order_by('-timestamp')
    
    # Add edit count to each message
    messages_with_counts = []
    for message in edited_messages:
        edit_history_qs = MessageHistory.objects.filter(message=message).order_by('-edited_at')
        edit_count = edit_history_qs.count()
        last_history = edit_history_qs.first()
        messages_with_counts.append({
            'message': message,
            'edit_count': edit_count,
            'last_edited': last_history.edited_at if last_history else None,
        })
        })
    
    context = {
        'messages_with_edits': messages_with_counts,
        'total_edited_messages': len(messages_with_counts),
    }
    
    return render(request, 'django_chat/messages_with_edits.html', context)


@login_required
def api_message_history(request, message_id):
    """
    API endpoint to get message edit history as JSON.
    Useful for AJAX requests to show edit history dynamically.
    """
    message = get_object_or_404(Message, id=message_id)
    
    # Check permissions
    if message.sender != request.user and message.receiver != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    # Get timeline data
    timeline = get_message_edit_timeline(message_id)
    
    # Format for JSON response
    history_data = []
    for entry in timeline:
        history_data.append({
            'content': entry['content'],
            'timestamp': entry['timestamp'].isoformat() if entry['timestamp'] else None,
            'is_current': entry['is_current'],
            'editor': entry['editor'].username if entry['editor'] else None,
            'edited_at': entry['edited_at'].isoformat() if entry['edited_at'] else None,
        })
    total_edits = MessageHistory.objects.filter(message=message).count()
    return JsonResponse({
        'message_id': message_id,
        'current_content': message.content,
        'is_edited': message.edited,
        'total_edits': total_edits,
        'history': history_data,
    })


# Utility view for demonstrating the signal in action
@login_required
def test_edit_signal(request):
    """
    Test view to demonstrate the edit logging signal.
    Creates a message and then edits it to show the signal working.
    """
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            # Create a test message
            test_message = Message.objects.create(
                sender=request.user,
                receiver=request.user,  # Send to self for testing
                content="This is a test message for demonstrating edit history."
            )
            messages.success(request, f'Test message created with ID: {test_message.id}')
            
        elif action == 'edit':
            message_id = request.POST.get('message_id')
            new_content = request.POST.get('new_content')
            
            try:
                test_message = Message.objects.get(id=message_id, sender=request.user)
                old_content = test_message.content
                
                # This edit will trigger the pre_save signal
                test_message.content = new_content
                test_message.save()
                
                messages.success(
                    request, 
                    f'Message edited! Signal logged old content: "{old_content[:30]}..."'
                )
                
            except Message.DoesNotExist:
                messages.error(request, 'Message not found or you do not have permission to edit it.')
    
    # Get user's test messages for the form
    user_messages = Message.objects.filter(
        sender=request.user, 
        receiver=request.user
    ).order_by('-timestamp')[:5]
    
    context = {
        'user_messages': user_messages,
    }
    
    return render(request, 'django_chat/test_edit_signal.html', context)
