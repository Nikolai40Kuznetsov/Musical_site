from django.db import models
from datetime import datetime


# Create your models here.
class Article(models.Model):
    article_id = models.CharField(max_length=20, verbose_name="ID", primary_key=True)
    article_title = models.CharField(max_length=20, verbose_name="Заголовок", null=False, default='Шаблон заголовка')
    article_annotation = models.CharField(max_length=200, verbose_name="Аннотация", null=False, default='Loren ipsum')
    article_preview_image = models.BinaryField(verbose_name="Превью",null=False, default=b'')
    article_text = models.TextField(verbose_name="Текст статьи",null=False, default='Loren ipsum')
    creation_date = models.DateTimeField(verbose_name="Дата", null=False, default=datetime.now())
    #article_author_id = models.OneToOneField(auth_user, on_delete=models.CASCADE)

    def __str__(self):
        return f'Новость: {self.article_title}'


    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class Article_Picture(models.Model):
    picture_id = models.CharField(max_length=20, verbose_name='Идентификатор изображения', primary_key=True)
    article_id = models.ForeignKey(Article, verbose_name='Идентификатор новости', on_delete=models.CASCADE)
    picture = models.BinaryField(null=False, verbose_name='Изображение', default=b'')

    def __str__(self):
        return f'Изображение: {self.article_id.article_title}'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'




