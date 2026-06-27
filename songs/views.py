from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import Song
from .forms import SongForm
from .decorators import admin_required
import json
from bson import ObjectId

def index(request):
    songs = Song.objects.all()
    paginator = Paginator(songs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'songs/index.html', {'page_obj': page_obj})

def load_more(request):
    page_number = request.GET.get('page', 1)
    songs = Song.objects.all()
    paginator = Paginator(songs, 10)
    page_obj = paginator.get_page(page_number)
    
    data = []
    for song in page_obj:
        data.append({
            'id': str(song._id),
            'title': song.title,
            'artist': song.artist,
            'genre': song.genre,
            'cover_image': song.cover_image.url if song.cover_image else None,
            'release_year': song.release_year,
            'rating': song.rating,
            'total_votes': song.total_votes,
            'star_rating': song.get_star_rating(),
            'has_voted': song.user_has_voted(request.user.id) if request.user.is_authenticated else False,
        })
    
    return JsonResponse({
        'songs': data,
        'has_next': page_obj.has_next(),
        'next_page': page_number + 1 if page_obj.has_next() else None
    })

@login_required
def song_detail(request, pk):
    try:
        song = Song.objects.get(_id=ObjectId(pk))
    except (Song.DoesNotExist, Exception):
        messages.error(request, 'Песня не найдена')
        return redirect('songs:index')
    return render(request, 'songs/song_detail.html', {'song': song})

@login_required
@csrf_exempt
def vote_song(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        song = Song.objects.get(_id=ObjectId(pk))
    except (Song.DoesNotExist, Exception):
        return JsonResponse({'error': 'Song not found'}, status=404)
    
    try:
        data = json.loads(request.body) if request.body else request.POST
        rating = data.get('rating')
        
        if rating is None:
            return JsonResponse({'error': 'Rating is required'}, status=400)
        
        rating = float(rating)
        if rating < 0 or rating > 10:
            return JsonResponse({'error': 'Rating must be between 0 and 10'}, status=400)
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid rating format'}, status=400)
    
    if song.user_has_voted(request.user.id):
        return JsonResponse({'error': 'Вы уже голосовали за этот трек'}, status=400)
    
    if song.add_vote(request.user.id, rating):
        return JsonResponse({
            'success': True,
            'message': 'Ваш голос учтен!',
            'new_rating': float(song.rating),
            'new_total_votes': song.total_votes,
            'star_rating': song.get_star_rating()
        })
    else:
        return JsonResponse({'error': 'Ошибка при голосовании'}, status=400)

@admin_required
def song_create(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.created_by = request.user
            song.votes = {}
            song.save()
            messages.success(request, f'Песня "{song.title}" успешно добавлена!')
            return redirect('songs:song_detail', pk=str(song._id))
    else:
        form = SongForm()
    return render(request, 'songs/song_create.html', {'form': form})

@admin_required
def song_update(request, pk):
    try:
        song = Song.objects.get(_id=ObjectId(pk))
    except (Song.DoesNotExist, Exception):
        messages.error(request, 'Песня не найдена')
        return redirect('songs:index')
    
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            messages.success(request, f'Песня "{song.title}" успешно обновлена!')
            return redirect('songs:song_detail', pk=str(song._id))
    else:
        form = SongForm(instance=song)
    return render(request, 'songs/song_update.html', {'form': form, 'song': song})

@admin_required
def song_delete(request, pk):
    try:
        song = Song.objects.get(_id=ObjectId(pk))
    except (Song.DoesNotExist, Exception):
        messages.error(request, 'Песня не найдена')
        return redirect('songs:index')
    
    if request.method == 'POST':
        title = song.title
        song.delete()
        messages.success(request, f'Песня "{title}" успешно удалена!')
        return redirect('songs:index')
    return render(request, 'songs/song_delete.html', {'song': song})