from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.authentication import BaseAuthentication
from decouple import config

class IsGuestandAuthenticate(BasePermission):
    """
    Allows access only to authenticated and Guest users.
    """

    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization', '')

        guestToken = config('GUEST_TOKEN')

        if auth_header == f"Bearer {guestToken}":
            return True
        elif auth_header.startswith("Bearer "):
            jwt_auth = JWTAuthentication()
            try:
                raw_token = auth_header.split()[1]
                validated_token = jwt_auth.get_validated_token(raw_token)
                request.user = jwt_auth.get_user(validated_token)
                return True
            except (InvalidToken, TokenError):
                return False

        return False
    
class NoAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return None