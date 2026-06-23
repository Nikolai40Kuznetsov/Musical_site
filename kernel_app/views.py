import base64
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.models import User
from kernel_app.models import Article, Article_Picture
from kernel_app.forms import NewArticleForm, LoginForm, RegistrationForm
from kernel_app.logger import Logger

logger = Logger()


def login(request):
    # Если пользователь уже авторизован, перенаправляем на новости
    if request.user.is_authenticated:
        return redirect('news')
    
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                logger.log_info(f"Пользователь {username} вошел в систему")
                # Перенаправляем на страницу, с которой пришел пользователь, или на новости
                next_url = request.GET.get('next', 'news')
                return redirect(next_url)
    
    return render(request, 'login.html', {'form': form})


def register(request):
    # Если пользователь уже авторизован, перенаправляем на новости
    if request.user.is_authenticated:
        return redirect('news')
    
    form = RegistrationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            # Автоматически входим после регистрации
            auth_login(request, user)
            logger.log_info(f"Зарегистрирован новый пользователь: {user.username}")
            return redirect('news')
    
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logger.log_info(f"Пользователь {request.user.username} вышел из системы")
    logout(request)
    return redirect('login')


@login_required
def main_page(request):
    logger.log_info("Зашли на страницу kernel_app/home")
    return HttpResponse("<h1>Hello world</h1>")


def page404(request, exception):
    logger.log_error('Ошибка 404')
    context = {}
    try:
        with open('static/images/404.jpg', 'rb') as image_file:
            en_str = base64.b64encode(image_file.read()).decode('utf-8')
            context['picture'] = en_str
    except FileNotFoundError:
        pass
    return render(request, '404.html', context)

@login_required
def news(request):
    logger.log_info(f"Пользователь {request.user.username} зашел на страницу новостей")
    limit_param = request.GET.get('limit')

    try:
        limit = int(limit_param) if limit_param else None
    except ValueError:
        limit = None

    if limit:
        news_list = Article.objects.all()[:limit]
    else:
        news_list = Article.objects.all()

    for news_item in news_list:
        if news_item.article_preview_image:
            news_item.imageBase = base64.b64encode(news_item.article_preview_image).decode('utf-8')

    context = {
        'newsList': news_list,
        'current_limit': limit,
        'colNews': len(news_list),
        'user': request.user
    }
    return render(request, 'news.html', context)


@login_required
def create_article(request):
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            preview = form.cleaned_data['article_preview_image'].read()
            pictures = form.cleaned_data.get('article_pictures', [])
            article_id = str(uuid.uuid4())[:20]

            article = Article(
                article_id=article_id,
                article_title=form.cleaned_data['article_title'],
                article_annotation=form.cleaned_data['article_annotation'],
                article_preview_image=preview,
                article_text=form.cleaned_data['article_text']
            )
            article.save()
            logger.log_info(f"Пользователь {request.user.username} создал новость ID:{article_id}")

            for picture in pictures:
                Article_Picture.objects.create(
                    picture_id=str(uuid.uuid4())[:20],
                    article_id=article,
                    picture=picture.read()
                )
            return redirect('news')

    form = NewArticleForm()
    return render(request, 'new_article_v2.html', {'form': form, 'user': request.user})


@login_required
def one_news(request, article_id):
    article = get_object_or_404(Article, article_id=article_id)
    db_pictures = Article_Picture.objects.filter(article_id=article)

    picture_list = []
    for pic in db_pictures:
        if pic.picture:
            picture_list.append(base64.b64encode(pic.picture).decode('utf-8'))

    context = {
        'article': article,
        'picture_list': picture_list,
        'len': len(picture_list),
        'user': request.user
    }
    logger.log_info(f"Пользователь {request.user.username} открыл новость ID:{article_id}")
    return render(request, 'one_news.html', context)