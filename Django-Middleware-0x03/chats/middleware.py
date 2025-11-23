import logging
from datetime import datetime

from django.utils.deprecation import MiddlewareMixin

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Log to file requests.log
file_handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class RequestLoggingMiddleware:
    """
    Middleware that logs each user's request with timestamp, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Determine username or 'Anonymous' if not authenticated
        user = request.user if hasattr(request, "user") and request.user.is_authenticated else "Anonymous"

        # Log timestamp, user, and path
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Continue processing the request
        response = self.get_response(request)
        return response


from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the chat outside 6AM - 9PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Restrict access: only allow 6AM <= hour < 21 (9PM)
        if request.path.startswith("/chats/") and not (6 <= current_hour < 21):
            return HttpResponseForbidden("Chat access is only allowed between 6AM and 9PM.")

        # Continue normal processing
        response = self.get_response(request)
        return response


import time
from django.http import JsonResponse

class OffensiveLanguageMiddleware:
    """
    Middleware that limits chat messages sent from a single IP.
    Maximum: 5 messages per minute.
    """

    # Class-level store for IP tracking
    ip_message_log = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only limit POST requests to chat endpoints
        if request.method == "POST" and request.path.startswith("/chats/"):
            ip = self.get_client_ip(request)
            now = time.time()

            # Initialize record for IP
            if ip not in self.ip_message_log:
                self.ip_message_log[ip] = []

            # Filter out messages older than 60 seconds
            self.ip_message_log[ip] = [timestamp for timestamp in self.ip_message_log[ip] if now - timestamp < 60]

            if len(self.ip_message_log[ip]) >= 5:
                # Too many requests
                return JsonResponse(
                    {"detail": "Rate limit exceeded: max 5 messages per minute."},
                    status=429
                )

            # Record current request timestamp
            self.ip_message_log[ip].append(now)

        # Continue processing request
        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """Extract client IP address from request"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip



from django.http import HttpResponseForbidden

class RolepermissionMiddleware:
    """
    Middleware that restricts access to specific actions based on user role.
    Only users with role 'admin' or 'moderator' are allowed.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define protected paths
        protected_paths = [
            "/chats/delete/",    # Example endpoint
            "/chats/admin/",     # Admin-only endpoints
        ]

        # Check if request path is protected
        if any(request.path.startswith(path) for path in protected_paths):
            user = getattr(request, "user", None)

            if not user or not user.is_authenticated:
                return HttpResponseForbidden("You must be logged in to perform this action.")

            # Check role
            if getattr(user, "role", "").lower() not in ["admin", "moderator"]:
                return HttpResponseForbidden("You do not have permission to perform this action.")

        # Proceed normally
        response = self.get_response(request)
        return response