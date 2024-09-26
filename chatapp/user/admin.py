from django.contrib import admin
from django.contrib.auth import get_user_model

from user.models import ChatGroup, Chat

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (["username", "email", "profile"])

@admin.register(ChatGroup)
class UserAdmin(admin.ModelAdmin):
    list_display = (["name"])


@admin.register(Chat)
class UserAdmin(admin.ModelAdmin):
    list_display = (["group","sender","message"])