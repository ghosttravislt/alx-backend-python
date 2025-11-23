from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission: Users can access ONLY their own messages
    and conversations.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # --- For Message model ---
        # If your Message model has sender and receiver fields
        if hasattr(obj, "sender") and hasattr(obj, "receiver"):
            return obj.sender == user or obj.receiver == user

        # --- For Conversation model ---
        # If Conversation has many-to-many participants
        if hasattr(obj, "participants"):
            return user in obj.participants.all()

        return False



from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API.
    - Only participants of a conversation can view, create, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj may be:
        - a Message instance (obj.conversation)
        - a Conversation instance itself
        """
        user = request.user

        # If the object is a Message model
        if hasattr(obj, "conversation"):
            return user in obj.conversation.participants.all()

        # If the object is a Conversation model
        if hasattr(obj, "participants"):
            return user in obj.participants.all()

        return False
