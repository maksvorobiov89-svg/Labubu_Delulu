from django.db import models
from django.contrib.auth.models import User

# Модель Post
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Зміст")
    author = models.CharField(max_length=100, verbose_name="Автор", default="Анонім")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публікації")
    category = models.CharField(max_length=100, verbose_name="Категорія")

    def __str__(self):
        return self.title

# Модель Comment
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Пост")
    author_name = models.CharField(max_length=100, verbose_name="Автор коментаря")
    content = models.TextField(verbose_name="Зміст коментаря")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return f'Коментар від {self.author_name} до {self.post.title}'