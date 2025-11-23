#!/usr/bin/env python3
from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    # Required fields for validation (example)
    display_name = serializers.CharField(source="first_name", read_only=True)

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "display_name",  # Added example char field
        ]


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""

    sender = UserSerializer(read_only=True)

    # Example of SerializerMethodField
    short_message = serializers.SerializerMethodField()

    def get_short_message(self, obj):
        """Returns the first 30 characters of the message."""
        return obj.message_body[:30]

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "sent_at",
            "short_message",  # Added method field
        ]


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation with nested messages."""

    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    # Example validation using serializers.ValidationError
    def validate(self, data):
        """Ensure a conversation has at least one participant."""
        if not hasattr(self.instance, "participants") or self.instance.participants.count() == 0:
            raise serializers.ValidationError("Conversation must have at least one participant.")
        return data

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
        ]
