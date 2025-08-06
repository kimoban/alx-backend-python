"""
Django filters for the messaging app.
"""

import django_filters
from django.db.models import Q
from .models import Message, Conversation, User


class MessageFilter(django_filters.FilterSet):
    """
    Filter for Message model
    """
    conversation = django_filters.CharFilter(field_name='conversation__id', lookup_expr='exact')
    sender = django_filters.CharFilter(field_name='sender__id', lookup_expr='exact')
    sender_username = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    message_body = django_filters.CharFilter(field_name='message_body', lookup_expr='icontains')
    sent_after = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    sent_date = django_filters.DateFilter(field_name='sent_at', lookup_expr='date')
    
    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'sender_username', 'message_body', 'sent_after', 'sent_before', 'sent_date']


class ConversationFilter(django_filters.FilterSet):
    """
    Filter for Conversation model
    """
    participant = django_filters.CharFilter(method='filter_by_participant')
    participant_username = django_filters.CharFilter(method='filter_by_participant_username')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    created_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date')
    has_messages = django_filters.BooleanFilter(method='filter_has_messages')
    
    def filter_by_participant(self, queryset, name, value):
        """
        Filter conversations by participant ID
        """
        return queryset.filter(participants__id=value)
    
    def filter_by_participant_username(self, queryset, name, value):
        """
        Filter conversations by participant username
        """
        return queryset.filter(participants__username__icontains=value)
    
    def filter_has_messages(self, queryset, name, value):
        """
        Filter conversations that have or don't have messages
        """
        if value:
            return queryset.filter(messages__isnull=False).distinct()
        else:
            return queryset.filter(messages__isnull=True)
    
    class Meta:
        model = Conversation
        fields = ['participant', 'participant_username', 'created_after', 'created_before', 'created_date', 'has_messages']


class UserFilter(django_filters.FilterSet):
    """
    Filter for User model
    """
    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    role = django_filters.ChoiceFilter(choices=User.ROLE_CHOICES)
    is_active = django_filters.BooleanFilter()
    date_joined_after = django_filters.DateTimeFilter(field_name='date_joined', lookup_expr='gte')
    date_joined_before = django_filters.DateTimeFilter(field_name='date_joined', lookup_expr='lte')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined_after', 'date_joined_before']
