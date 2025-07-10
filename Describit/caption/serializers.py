from rest_framework import serializers
from rest_framework import exceptions
from allauth.account.adapter import get_adapter
from Describit import settings
from .models import CaptionResult
from useracc.models import User
from allauth.account.utils import setup_user_email
from rest_framework_simplejwt.tokens import RefreshToken

class CaptionListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CaptionResult
        fields = ['id','caption', 'image']

    def get_photo_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)

class GenerateCaptionSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
    metadata = serializers.JSONField(required=False, allow_null=True)

class SaveCaptionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    caption = serializers.CharField(required=True, allow_blank=True)
    author = serializers.CharField(required=False, allow_blank=True)
    date = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    device = serializers.CharField(required=False, allow_blank=True)
    model = serializers.CharField(required=False, allow_blank=True)
    image = serializers.ImageField(required=True)
    uid = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, data):
        if not data.get('caption') or not data['caption'].strip():
            raise ValueError('Caption is Required.')
        if not data.get('image'):
            raise serializers.ValidationError('Image is required.')
        return data
    
    def create(self, validated_data):
        user = self.context.get('request').user

        caption_result = CaptionResult.objects.create(
            caption=validated_data.get('caption'),
            author=validated_data.get('author', ''),
            date=validated_data.get('date', None),
            location=validated_data.get('location', ''),
            device=validated_data.get('device', ''),
            model=validated_data.get('model', ''),
            image=validated_data.get('image'),
            uid=user 
        )

        caption_result.save()
        return caption_result
    
class DetailCaptionSerializer(serializers.ModelSerializer):
    caption = serializers.CharField(required=True)
    author = serializers.CharField(required=False)
    date = serializers.CharField(required=False)
    location = serializers.CharField(required=False)
    device = serializers.CharField(required=False)
    model = serializers.CharField(required=False)
    class Meta:
        model = CaptionResult
        fields = '__all__'
    
    def get_photo_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)
    
    def update(self, instance, validated_data):
        instance.caption = validated_data.get('caption', instance.caption)
        instance.author = (
            validated_data['author'] if validated_data.get('author') not in ["", None] else None
        )
        instance.date =  (
            validated_data['date'] if validated_data.get('date') not in ["", None] else None
        )
        instance.location = (
            validated_data['location'] if validated_data.get('location') not in ["", None] else None
        )
        instance.device = (
            validated_data['device'] if validated_data.get('device') not in ["", None] else None
        )
        instance.model = (
            validated_data['model'] if validated_data.get('model') not in ["", None] else None
        )

        
        instance.save()
        return instance
