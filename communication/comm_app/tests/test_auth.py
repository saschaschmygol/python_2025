import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


@pytest.mark.django_db
class AuthTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.url = "/api/operator/tickets_user/"

    def test_unauthenticated_access(self):
        """Тест: Доступ без аутентификации — 401"""
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "detail" in response.data  # Проверяем, что есть ошибка (DRF-стиль)

    def test_authenticated_access(self):
        """Тест: Доступ с аутентификацией — 200"""
        # Логинимся (force_authenticate имитирует токен/сессию)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert isinstance(
            response_data, list
        )  # Ожидаем список (пустой, если нет данных)

    def test_logout_like(self):
        """Опционально: Проверяем, что после 'выхода' — снова 401"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        assert response.status_code == 200

        # 'Выходим' (снимаем аутентификацию)
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        assert response.status_code == 401
