from django.shortcuts import render

# Create your views here.
#!/usr/bin/env python3
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
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




from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Chats / messaging routes
    path('api/chats/', include('messaging_app.chats.urls')),
]
