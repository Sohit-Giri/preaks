
# myapp/admin.py
from django.contrib import admin
from .models import Forum, OTP

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "genre", "created_at")
    search_fields = ("title", "author", "genre")
    list_filter = ("genre", "created_at")

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    listdisplay = ("email", "code")
    search_fields = ("email", "code")