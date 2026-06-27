from django.urls import path, re_path
from . import views

app_name = 'songs'

urlpatterns = [
    path('', views.index, name='index'),
    path('load-more/', views.load_more, name='load_more'),
    re_path(r'^song/(?P<pk>[a-fA-F0-9]{24})/$', views.song_detail, name='song_detail'),
    re_path(r'^song/(?P<pk>[a-fA-F0-9]{24})/vote/$', views.vote_song, name='vote_song'),
    path('song/create/', views.song_create, name='song_create'),
    re_path(r'^song/(?P<pk>[a-fA-F0-9]{24})/update/$', views.song_update, name='song_update'),
    re_path(r'^song/(?P<pk>[a-fA-F0-9]{24})/delete/$', views.song_delete, name='song_delete'),
]