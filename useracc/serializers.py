import os
from Descripix import settings
from rest_framework import serializers, exceptions
from rest_framework.exceptions import AuthenticationFailed
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from .models import User
from . import google
from datetime import date
import random

class GoogleSocialAuthSerializer(serializers.Serializer):
    googleId = serializers.CharField()

    def validate_googleId(self, googleId):

        user_data = google.Google.validate(googleId)

        try:
            if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
                raise AuthenticationFailed("The token is not valid for this application")
            print("this running")
        except:
            raise AuthenticationFailed("The token is either invalid or has expired")
        
        try:
            print("sub: ", user_data['sub'])
            user_data['sub']
        except:
            raise exceptions.ValidationError("The touken is either invalid or has expired")

        try:
            google_id = user_data['sub']
            email = user_data['email']
            username = user_data['name']
            photoUrl = user_data['picture']
            provider = 'google'

        except KeyError as e:
            raise exceptions.ValidationError(f"Missing field in user data: {str(e)}")
        print("its done")
        return self.register_social_user(provider=provider, google_id=google_id, email= email, name= username, photoUrl=photoUrl)
    
    def generate_username(self, name, user_id=None):
        username = name
        if not User.objects.filter(username=username).exclude(id=user_id).exists():
            return username
        else:
            random_username = username + str(random.randint(0, 1000))
            return self.generate_username(random_username)


    def register_social_user(self, provider, google_id, email, name, photoUrl=None):
        user_qs = User.objects.filter(email=email)
        socialAccount =  SocialAccount.objects.filter(provider=provider,uid=google_id)

        if user_qs.exists():
            user = user_qs.first()
            if socialAccount.exists():
                print("social account exists")
                social_account = socialAccount.first()
                if social_account.user == user:
                    print("social account user match")
                    user.id = google_id
                    user.username = self.generate_username(name, google_id)
                    user.profile_img = photoUrl
                    user.save()
                    token = user.tokens()
                    return {
                        'refresh': token.get('refresh'),
                        'access': token.get('access')}

            else:
                raise AuthenticationFailed('Social account does not match with user')
        else:
            print("new_user")

            adapter = get_adapter()
            new_user = adapter.new_user(None)
            new_user.id = google_id
            new_user.username = self.generate_username(name)
            new_user.email = email
            new_user.profile_img = photoUrl
            new_user.set_unusable_password()
            new_user.is_active = True
            new_user.is_verified = True
            new_user.save()

            EmailAddress.objects.create(
                user=new_user,
                email=email,
                verified=True,
                primary=True
            )

            SocialAccount.objects.create(
                user=new_user,
                provider=provider,
                uid=google_id,
                extra_data={ 
                    'name': name,
                    'picture': photoUrl,
                    'email': email
                }  
            )
            
            token = new_user.tokens()
            return {
                'refresh': token.get('refresh'),
                'access': token.get('access')}


class UserDetailsSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(format='%d-%m-%Y')
    """
    User model w/o password
    """
    class Meta:
        model = User
        fields = ('id','username', 'email', 'gender','birth_date', 'about_me', 'profile_img')
        read_only_fields = ('email',)


class EditUserSerializer(serializers.Serializer):
    gender = serializers.CharField()
    birth_date = serializers.DateField(input_formats=['%d-%m-%Y'], allow_null=True)
    about_me = serializers.CharField()

    def validate(self, data):
        user = self.context.get('request').user
        birth_date = data.get('birth_date')
        gender = data.get('gender')

        if birth_date and birth_date > date.today():
            raise ValueError("Date of birth cannot be in the future.")
        
        valid_genders = ['male', 'female', 'rather not say']
        if gender and gender not in valid_genders:
            raise ValueError("Invalid gender, must be male, female or rather not say")
        
        return super().validate(data)
    

    def get_cleaned_data(self):
        return {
            'gender': self.validated_data.get('gender', self.instance.gender),
            'birth_date': self.validated_data.get('birth_date', self.instance.birth_date),
            'about_me': self.validated_data.get('about_me', self.instance.about_me),
        }
    
    def update(self, instance, validated_data):

        instance.gender = validated_data.get('gender') or None
    
        instance.birth_date = validated_data.get('birth_date') or None
        instance.about_me = validated_data.get('about_me') or None
        
        instance.save()
        return instance