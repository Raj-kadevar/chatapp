from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.models import TimeStampedModel

class User(AbstractUser):
    profile = models.ImageField(blank=True, null=True, upload_to="profile/")
    status = models.BooleanField(default=False, blank=True, null=True)
    tune = models.FileField(default="audio/beep.mp3",blank=True,null=True)

class ChatGroup(TimeStampedModel):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name


class Chat(models.Model):
    message = models.CharField(max_length=5000, blank=True, null=True)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    images = models.FileField(blank=True, null=True, upload_to="profile/")