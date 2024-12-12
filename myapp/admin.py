from django.contrib import admin
from .models import Forum

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "genre", "created_at"]
    search_fields = ["title", "author", "genre"]
    list_filter = ["genre", "created_at"]