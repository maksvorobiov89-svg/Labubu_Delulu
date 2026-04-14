from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm, CommentForm # Імпортуємо наші нові форми

# 1. функція для показу всіх постів
def post_list(request):
    posts = Post.objects.all().order_by('-pub_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

# 2. функція створення поста
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save() # Зберігаємо пост в базу
            return redirect('post_list') # Повертаємо на головну сторінку
    else:
        form = PostForm() # Показуємо порожню форму
    return render(request, 'blog/post_edit.html', {'form': form})

# 3. Функція додавання коментаря
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk) # Шукаємо пост, до якого пишуть коментар
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # "Почекай, не зберігай!"
            comment.post = post               # "Ось до цього поста прив'яжи коментар"
            comment.save()                    # "Тепер зберігай!"
            return redirect('post_list')
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})