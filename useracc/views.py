
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView, TokenVerifyView
from rest_framework import status, exceptions
from .serializers import GoogleSocialAuthSerializer, UserDetailsSerializer, EditUserSerializer
import time
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import requests
# Create your views here.
    
class GoogleSocialAuthView(APIView):
    permission_classes = [AllowAny]
    serializer_class = GoogleSocialAuthSerializer
    def post(self, request, *args, **kwargs):
        """
        POST with Auth Token from Google
        """
        serializer = self.serializer_class(data=request.data)
        print("testt")
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['googleId'])
        return Response(
            {
                "status": True,
                "message": "login successful",
                "data": data
            },
            status=status.HTTP_201_CREATED
        )
    
    def handle_exception(self, exc):
        if isinstance(exc, exceptions.AuthenticationFailed):
            detail = exc.detail
            if isinstance(detail, dict) and "detail" in detail:
                message = detail["detail"]
            else:
                message = str(detail)

            return Response(
                {"status": False, 
                 "message": message
                 },
                status=status.HTTP_401_UNAUTHORIZED
            )
        elif hasattr(exc, 'detail'):
            return Response(
                {
                    "status": False,
                    "message": exc.detail
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                "status": False,
                "message": str(exc)  
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    

class CostumLoginTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        return Response(
            {
                "status": True,
                "message": "Token refreshed successfully",
                "data": response.data
            },
            status=status.HTTP_200_OK
        )

    def handle_exception(self, exc):
        if isinstance(exc, exceptions.AuthenticationFailed):
            return Response(
                {"status": False, 
                 "message": "Session is invalid or expired"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        elif hasattr(exc, 'detail'):
            return Response(
                {
                    "status": False,
                    "message": exc.detail
                },
            )
        return Response(
            {
                "status": False,
                "message": str(exc)  
            },
        )
class CostumLoginTokenVerifyView(APIView):
    def get(self, request, *args, **kwargs):
        
        return Response(
            {
                "status": True,
                "message": "Token verified successfully",
            },
            status=status.HTTP_200_OK
        )
    def handle_exception(self, exc):
        if isinstance(exc, exceptions.AuthenticationFailed):
            return Response(
                {"status": False, 
                 "message": "Token is Already Expired"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {
                "status": False,
                "message": str(exc)  
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class CostumLogoutView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)  
        return Response(
            {
                "status": True,
                "message": "Logout successful"
            },
            status=status.HTTP_200_OK
        )

    def handle_exception(self, exc):
        if isinstance(exc, exceptions.AuthenticationFailed):
            return Response(
                {"status": True, 
                 "message": "Session is invalid or expired"},
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "status": False,
                "message": str(exc)  
            },
            status=status.HTTP_400_BAD_REQUEST
        )
class CostumUserDetailsView(APIView):
    serializer_class = UserDetailsSerializer
    def get(self, request):
        user = request.user
        serializer = UserDetailsSerializer(user, context={"request": request})

        return Response(
            {
                "status": True,
                "message": "User details retrieved successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def handle_exception(self, exc):
        if isinstance(exc, exceptions.AuthenticationFailed):
            return Response(
                {"status": False, 
                 "message":exc.detail if hasattr(exc, 'detail') else "Session is invalid or expired"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {
                "status": False,
                "message": str(exc)  
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
class CostumEditUserView(APIView):
    serializer_class = EditUserSerializer

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "status": True,
                "message": "User details updated successfully",
            },
            status=status.HTTP_200_OK
        )

        
    def handle_exception(self, exc):
        if isinstance(exc, exceptions.AuthenticationFailed):
            return Response(
                {"status": False, 
                 "message": "Session is invalid or expired"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {
                "status": False,
                "message": str(exc)  
            },
            status=status.HTTP_400_BAD_REQUEST
        )