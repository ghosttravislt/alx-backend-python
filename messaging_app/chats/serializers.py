#!/usr/bin/env python3
from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ["user_id", "first_name", "last_name", "email", "phone_number", "role"]


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["message_id", "sender", "message_body", "sent_at"]


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation with nested messages."""
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "messages", "created_at"]
