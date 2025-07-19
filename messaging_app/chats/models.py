import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(
        unique=True,
        verbose_name='email address',
        help_text="User's email address"
    )
    
    first_name = models.CharField(
        max_length=150,
        blank=False,  # Making required (default is blank=True)
        verbose_name='first name'
    )
    
    last_name = models.CharField(
        max_length=150,
        blank=False,  # Making required (default is blank=True)
        verbose_name='last name'
    )
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    
    class Meta:
        indexes = [
            models.Index(fields=['id'], name='user_id_index'),
        ]

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='conversation_id_index'),
        ]

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='message_id_index'),
            models.Index(fields=['sender'], name='message_sender_index'),
            models.Index(fields=['conversation'], name='message_conversation_index'),
        ]
