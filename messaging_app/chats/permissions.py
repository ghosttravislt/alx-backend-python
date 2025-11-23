from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Allows access only to the owner of the object.
    Example: A user can only view their own messages or conversations.
    """

    def has_object_permission(self, request, view, obj):
        # If message has sender or receiver fields:
        if hasattr(obj, "sender") and hasattr(obj, "receiver"):
            return obj.sender == request.user or obj.receiver == request.user
        
        # For conversation objects with participants:
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        return False
