from django.contrib import admin
from .models import Song

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre', 'rating', 'total_votes', 'release_year']
    search_fields = ['title', 'artist']
    list_filter = ['genre', 'is_single', 'release_year']
    readonly_fields = ['rating', 'total_votes', 'votes', 'created_at', 'updated_at']