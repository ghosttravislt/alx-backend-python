from django.db import models

# Create your models here.

#!/usr/bin/env python3
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model extending Django AbstractUser."""
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    ROLE_CHOICES = [
        ("guest", "Guest"),
        ("host", "Host"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="guest")

    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]


class Conversation(models.Model):
    """Conversation between two or more users."""
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    """Messages stored within conversations."""
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_sent")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
