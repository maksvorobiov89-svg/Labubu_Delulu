from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

# Імпортуємо серіалайзери, дозволи та моделі
from .models import Post
from .serializers import PostSerializer, RegisterSerializer
from .permissions import IsAdmin

class RegisterAPI(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Користувача успішно створено!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostListCreateAPI(APIView):
    # Додаємо кастомну перевірку! Тільки адміни можуть звертатися до цього API
    permission_classes = [IsAdmin]

    @swagger_auto_schema(responses={200: PostSerializer(many=True)})
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PostSerializer)
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailAPI(APIView):
    # Додаємо безпеку і сюди, щоб ніхто чужий не міг видалити пост
    permission_classes = [IsAdmin]

    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    @swagger_auto_schema(responses={200: PostSerializer()})
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PostSerializer, responses={200: PostSerializer()})
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)