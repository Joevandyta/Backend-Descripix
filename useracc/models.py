from django.db import models
import os
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken

import uuid
# Create your models here.

class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_active,is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The username given is not valid')
        if email is None:
            raise TypeError('Users should have a Email')
        
        email = self.normalize_email(email)
        user = self.model(
            username = username, 
            email = email, 
            is_active = False,
            is_staff = is_staff,
            is_superuser = is_superuser,
            date_joined = now,
            **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, username, email, password= None, **extra_fields):
        return self._create_user(username, email, password, is_active= True, is_staff=False, is_superuser=False, **extra_fields)
    
    def create_superuser(self, username, email, password = None, **extra_fields):
        user = self._create_user(username, email, password, is_active= True, is_staff=True, is_superuser=True, **extra_fields)
        
        user.is_active = True
        user.save(using=self._db)
        return user
    
# AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
#                   'twitter': 'twitter', 'email': 'email'}

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    slug = slugify(instance.username)
    unique_id = uuid.uuid4().hex[:8]  # pendek agar tidak kepanjangan
    filename = f"{slug}-{unique_id}.{ext}"
    return os.path.join('profile_images/', filename)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(primary_key=True, max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    about_me = models.TextField(max_length=500, blank=True, null=True)
    profile_img = models.CharField(max_length=500, null=True, blank=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        print("Token Lifetime : ", refresh.payload.get("exp"))
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    
    # def save(self, *args, **kwargs):
    #     try:
    #         # Jika user sudah memiliki foto profil, hapus file lama sebelum update
    #         old_user = User.objects.get(pk=self.pk)
    #         if old_user.profile_img and old_user.profile_img != self.profile_img:
    #             old_user.profile_img.delete(save=True)
    #     except User.DoesNotExist:
    #         pass  # Jika user baru, tidak ada file lama yang dihapus
        
        super().save(*args, **kwargs)