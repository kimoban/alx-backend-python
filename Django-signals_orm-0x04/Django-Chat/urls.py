from django.urls import path
from . import Views

app_name = 'django_chat'

urlpatterns = [
    # Message detail with edit history
    path('message/<int:message_id>/', Views.message_detail_with_history, name='message_detail_with_history'),
    
    # Edit message (triggers pre_save signal)
    path('message/<int:message_id>/edit/', Views.edit_message_with_history, name='edit_message'),
    
    # View complete edit history
    path('message/<int:message_id>/history/', Views.message_edit_history, name='message_edit_history'),
    
    # Revert message to previous version
    path('message/<int:message_id>/revert/<int:history_id>/', Views.revert_message, name='revert_message'),
    
    # List messages with edits
    path('edited-messages/', Views.messages_with_edits, name='messages_with_edits'),
    
    # API endpoint for AJAX history loading
    path('api/message-history/<int:message_id>/', Views.api_message_history, name='api_message_history'),
    
    # Test edit signal functionality
    path('test-edit-signal/', Views.test_edit_signal, name='test_edit_signal'),
]
