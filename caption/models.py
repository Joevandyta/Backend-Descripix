from django.db import models
import os
from django.utils.text import slugify
from useracc.models import User

def caption_directory_path(instance, filename):

    if hasattr(instance, 'uid') and instance.uid:
        username = instance.uid.username  # Ambil username dari user
    else:
        username = "unknown_user"
    ext = filename.split('.')[-1]
    base_filename = slugify(username)
    new_filename = f"{base_filename}.{ext}"
    directory = 'caption_result/'

    counter = 1
    while os.path.exists(os.path.join(directory, new_filename)):
        print("File exists")
        new_filename = f"{base_filename}-{counter}.{ext}"
        counter += 1

    return os.path.join(directory, new_filename)

class CaptionResult(models.Model):
    caption = models.TextField()
    image = models.ImageField(upload_to=caption_directory_path, null=False)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    author = models.CharField(max_length=100, blank=True, null=True)
    date = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    device = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.caption
