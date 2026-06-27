from django import forms
from .models import Song

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'genre', 'cover_image', 'release_year', 
                 'lyrics', 'is_single', 'album_name']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'artist': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'lyrics': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'is_single': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'album_name': forms.TextInput(attrs={'class': 'form-control'}),
        }