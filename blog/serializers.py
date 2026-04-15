from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment

# 1. Серіалайзер для реєстрації
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}} # Пароль не повертається у відповіді

    def create(self, validated_data):
        # Використовуємо create_user, щоб пароль автоматично зашифрувався (хешувався)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# 2. Cеріалайзер з кастомною валідацією
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    # Кастомна валідація для поля title
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Помилка: Заголовок має містити щонайменше 5 символів.")
        if "спам" in value.lower():
            raise serializers.ValidationError("Помилка: Використання заборонених слів у заголовку.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'