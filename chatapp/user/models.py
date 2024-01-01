from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.models import TimeStampedModel

class User(AbstractUser):
    profile = models.ImageField(blank=True, null=True, upload_to="profile/")


class ChatGroup(TimeStampedModel):
    name = models.CharField(max_length=30)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="chat_group")

    def __str__(self):
        return self.name


class ChatMessage(TimeStampedModel):
    message = models.TextField(max_length=5000)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="as_sender")
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name="as_receiver")