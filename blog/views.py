from django.shortcuts import render
from .models import Post

def post_list(request):
    # Дістаємо всі пости з бази даних, сортуємо від найновіших до найстаріших
    posts = Post.objects.all().order_by('-pub_date')
    # Передаємо їх у HTML-шаблон
    return render(request, 'blog/post_list.html', {'posts': posts})