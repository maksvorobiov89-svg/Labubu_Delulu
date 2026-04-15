from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views, api_views
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name='post_new'), # Посилання для нового поста
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'), # Посилання для коментаря
    path('api/posts/', api_views.PostListCreateAPI.as_view(), name='api_post_list'),
    path('api/posts/<int:pk>/', api_views.PostDetailAPI.as_view(), name='api_post_detail'),
    path('api/register/', api_views.RegisterAPI.as_view(), name='api_register'),
    path('api/login/', obtain_auth_token, name='api_login'),
    path('api/posts/', api_views.PostListCreateAPI.as_view(), name='api_post_list'),
    path('api/posts/<int:pk>/', api_views.PostDetailAPI.as_view(), name='api_post_detail'),
]