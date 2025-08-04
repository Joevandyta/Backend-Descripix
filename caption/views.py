from django.shortcuts import render
from .serializers import CaptionListSerializer, GenerateCaptionSerializer, DetailCaptionSerializer, SaveCaptionSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CaptionResult
from useracc.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from Descripix import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from PIL import Image
import base64
from PIL.ExifTags import TAGS
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from .llama.llama_config import getCaption
import time
# Create your views here.

class SaveResultView(CreateAPIView):
    serializer_class = SaveCaptionSerializer
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()


        return Response({
                "status": True,
                "message": "Caption saved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED
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
                "status": "False",
                "message": str(exc)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
class GetAllResultView(ListAPIView):
    serializer_class = CaptionListSerializer
    def get_queryset(self):
        user = self.request.user

        return CaptionResult.objects.filter(uid=user.id)
    
    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {
                    "status": "True",
                    "message": "No captions found",
                },
                status=status.HTTP_200_OK
            )
        serializer = self.serializer_class(queryset, context={"request": request},many=True)

        return Response(
            {
                "status": True,
                "message": "List captions retrieved successfully",
                "data": serializer.data,
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
                "status": "False",
                "message": str(exc)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = GenerateCaptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        image = serializer.validated_data['image']
        text = serializer.validated_data.get('text', '')

        image = Image.open(image)
        exif_data = image.getexif()  # Ambil metadata EXIF
        exif_ifd = exif_data.get_ifd(0x8769)  # EXIF IFD

        metadata = {}
        for tag_id, value in exif_ifd.items():
            tag_name = TAGS.get(tag_id, tag_id)
            metadata[tag_name] = value

        return Response({
            "status": True,
            "message": "Metadata retrieved successfully",
            "data": {
                "metadata": metadata.items(),
            }
        })
    def handle_exception(self, exc):
        return Response(
            {
                "status": "False",
                "message": str(exc)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class CaptionGenerateView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):

        serializer = GenerateCaptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        metadata = serializer.validated_data.get('metadata', '')
        
        caption = getCaption(
            image_url= serializer.validated_data['image'],
            metadata = metadata,
            language_code = serializer.validated_data.get('language_code', 'en'))
        
        return Response({
            "status": True,
            "message": "Caption generated successfully",
            "data": {
                "caption": caption
            }
        },
            status=status.HTTP_200_OK
            )
    
    def handle_exception(self, exc):
        return Response(
            {
                "status": "False",
                "message": str(exc)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
class DetailCaptionView(APIView):
    serializer_class = DetailCaptionSerializer
    def put(self, request, *args, **kwargs):
        
        result_id = request.query_params["id"]
        caption_object = CaptionResult.objects.get(id=result_id)
        user = request.user
        if caption_object.uid != user:
            raise exceptions.PermissionDenied("You are not authorized to edit this caption")
        

        serializer = self.serializer_class(caption_object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "status": True,
                "message": "Caption updated successfully",
            },
            status=status.HTTP_200_OK
        )
    def delete(self, request, *args, **kwargs):
        result_id = request.query_params["id"]

        caption_object = CaptionResult.objects.get(id=result_id)
        user = request.user
        if caption_object.uid != user:
            raise exceptions.PermissionDenied("You are not authorized to edit this caption")
        
        caption_object.delete()
        return Response(
            {
                "status": True,
                "message": "Caption deleted successfully",
            }
        )


    def get(self, request, *args, **kwargs):
        result_id = request.query_params["id"]

        if not result_id:
            raise ValueError("parameter ID is required")
        
        caption_object = CaptionResult.objects.get(id=result_id)
        user = request.user
        if caption_object.uid != user:
            raise exceptions.PermissionDenied("You are not authorized to view this caption")
        
        serializer = self.serializer_class(caption_object, context={"request": request})
        return Response(
            {
                "status": True,
                "message": "Caption retrieved successfully",
                "data": serializer.data
            }
        )

    def handle_exception(self, exc):
        if isinstance(exc, exceptions.AuthenticationFailed):
            return Response(
                {"status": False, 
                 "message": "Session is invalid or expired"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if hasattr(exc, 'detail'):
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