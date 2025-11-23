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
