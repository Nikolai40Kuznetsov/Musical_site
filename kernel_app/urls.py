from django.urls import path
from kernel_app.views import (
    main_page, login, register, logout_view, page404, 
    news, create_article, one_news
)

urlpatterns = [
    path('', main_page, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('home/', main_page, name='main'),
    path('404/', page404, name='404'),
    path('news/', news, name='news'),
    path('new/', create_article, name='create_article'),
    path('news/<str:article_id>/', one_news, name='one_news'),
]