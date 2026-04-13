from django.urls import path
from . import views

urlpatterns = [
    # Порожній рядок '' означає головну сторінку додатку
    path('', views.post_list, name='post_list'),
]