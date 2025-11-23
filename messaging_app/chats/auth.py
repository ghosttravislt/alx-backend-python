from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Extend this class later if you want:
    - logging
    - custom token validation
    - user blocking checks
    """
    pass
