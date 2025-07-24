from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import QuerySet
from typing import Any

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer, UserRegistrationSerializer
from .permissions import IsParticipantOfConversation, IsMessageSenderOrParticipant, IsConversationParticipant
from .filters import MessageFilter, ConversationFilter # type: ignore
from .pagination import MessagePagination, ConversationPagination

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API view for user profile management
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self): # type: ignore
        """Return the current authenticated user"""
        return self.request.user


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsConversationParticipant]
    pagination_class = ConversationPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ConversationFilter
    search_fields = ['name']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self): # type: ignore
        """Only return conversations the authenticated user is part of"""
        if not self.request.user.is_authenticated:
            return Conversation.objects.none()
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """Automatically add the current user as a participant when creating a conversation"""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsMessageSenderOrParticipant]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['content']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']
    
    def get_queryset(self) -> QuerySet: # type: ignore
        """Only return messages from conversations the user is part of"""
        if not self.request.user.is_authenticated:
            return Message.objects.none()
            
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation').prefetch_related('conversation__participants')
    
    def perform_create(self, serializer):
        """Ensure the user is part of the conversation before creating a message"""
        conversation = serializer.validated_data['conversation']
        
        # Check if user is part of the conversation
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You're not part of this conversation")
        
        # Save with the current user as sender
        serializer.save(sender=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Delete a message with proper error handling"""
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"detail": "Message deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": "Failed to delete message"},
                status=status.HTTP_400_BAD_REQUEST
            )