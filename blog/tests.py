from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class BlogAPITests(APITestCase):

    def setUp(self):
        # Ця функція запускається ПЕРЕД кожним тестом. Створюємо двох юзерів: звичайного і адміна
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.admin = User.objects.create_superuser(username='adminuser', password='password123')
        self.register_url = '/api/register/'
        self.login_url = '/api/login/'
        self.posts_url = '/api/posts/'

    # 1. Тест реєстрації
    def test_user_registration(self):
        data = {'username': 'newuser', 'password': 'newpassword', 'email': 'new@mail.com'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # 2. Тест логіну (отримання токена)
    def test_user_login(self):
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    # 3. Тест кастомної перевірки IsAdmin (звичайний юзер отримує 403 Forbidden)
    def test_is_admin_permission(self):
        self.client.force_authenticate(user=self.user)  # Заходимо як звичайний юзер
        response = self.client.get(self.posts_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # 4. Тест кастомної перевірки IsAdmin (адмін отримує доступ 200 OK)
    def test_admin_access(self):
        self.client.force_authenticate(user=self.admin)  # Заходимо як адмін
        response = self.client.get(self.posts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 5. Тест кастомної валідації серіалайзера (короткий заголовок має викликати помилку 400)
    def test_title_validation(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'title': 'Ко',  # Менше 5 символів!
            'content': 'Тестовий текст',
            'author': 'Адмін',
            'category': 'Тест'
        }
        response = self.client.post(self.posts_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)  # Перевіряємо, що помилка саме в заголовку