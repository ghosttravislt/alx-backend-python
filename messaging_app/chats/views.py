from django.shortcuts import render

# Create your views here.
#!/usr/bin/env python3
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for listing and creating conversations."""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    @action(detail=True, methods=["post"])
    def add_message(self, request, pk=None):
        """Custom endpoint to send message to an existing conversation."""
        conversation = self.get_object()

        user_id = request.data.get("sender_id")
        message_body = request.data.get("message_body")

        if not user_id or not message_body:
            return Response({"error": "sender_id and message_body required"},
                            status=status.HTTP_400_BAD_REQUEST)

        sender = User.objects.get(user_id=user_id)
        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )
        return Response(MessageSerializer(message).data, status=201)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """List-only messages."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
