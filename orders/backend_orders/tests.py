from copy import deepcopy
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import User


class APITests(APITestCase):
    """
    Класс для тестирования работы представлений.
    """

    data = {
        'first_name': 'Mikhail',
        'last_name': 'Ivanov',
        'email': 'mikiv@ya.ru',
        'password': 'pass3450',
        'company': 'Company',
        'position': 'manager',

    }
    url_user_register = reverse('user-register')
    url_user_login = reverse('user-login')

    def setUp(self):
        return super().setUp()

    def create_test_user(self):
        data = deepcopy(self.data)
        password = data.pop('password')

        user = User.objects.create(**data, type='buyer')
        user.is_active = True
        user.set_password(password)
        user.save()

    def test_user_registration(self):
        """
        Проверка статуса ответа при регистрации пользователя.
        Представление RegisterAccount.
        """

        response = self.client.post(self.url_user_register, self.data)

        assert response.status_code == 201
        assert response.data['Status'] is True

    def test_user_reg_empty(self):
        """
        Проверка наличия незаполненных данных при регистрации. \
        Представление RegisterAccount.
        """

        data = deepcopy(self.data)
        data.pop('email')

        response = self.client.post(self.url_user_register, data)

        assert 'Errors' in response.data
        assert response.data['Errors'] == 'Необходимо заполнить все обязательные поля'
        assert response.status_code == 401

    def test_user_reg_valid(self):
        """
        Проверка параметров на валидацию при регистации пользователя.
        Представление RegisterAccount.
        """

        data = deepcopy(self.data)
        data['email'] = ''

        response = self.client.post(self.url_user_register, data)

        assert response.status_code == 422
        assert response.data['Status'] is False
        assert 'Errors' in response.data

    def test_new_user_registration_password_error(self):
        """
        Проверка пароля.
        Представление RegisterAccount.
        """

        data = deepcopy(self.data)
        data['password'] = ''
        response = self.client.post(self.url_user_register, data)

        assert response.status_code == 403
        assert response.data['Status'] is False
        assert 'Errors' in response.data

    def test_login_account(self):
        """
        Проверка статуса авторизации.
        Представление LoginAccount.
        """

        self.create_test_user()
        email = self.data['email']
        password = self.data['password']
        login_data = dict(email=email, password=password)
        response = self.client.post(self.url_user_login, login_data)

        assert response.status_code is 200
        assert 'Status' in response.data
        assert response.data['Status'] is True

    def test_login_empty_data(self):
        """
        Проверка заполнения обязательных полей при авторизации.
        Представление LoginAccount.
        """

        self.create_test_user()
        email = self.data['email']
        password = self.data['password']
        login_data = dict(email=email, password=password)
        login_data.pop('email')

        response = self.client.post(self.url_user_login, login_data)

        assert self.failureException == AssertionError
        assert response.status_code == 401

    def test_get_contact(self):
        """
        Тест метода GET на отсутсвие ошибок в данных ответа.
        Представление ContactView.
        """

        url_contact = reverse('user-contact')

        self.create_test_user()
        email = self.data['email']
        user = User.objects.get(email=email)
        token = Token.objects.get_or_create(user_id=user.id)[0].key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        response = self.client.get(url_contact, format='json')

        assert response.status_code == 200
        assert 'Errors' not in response.data

    def test_get_contact_anon(self):
        """
        Тест метода GET на проверку выполнения запроса неавторизованым пользователем,
        наличие в данных ответа ошибок.
        Представление ContactView.
        """

        url_contact = reverse('user-contact')
        response = self.client.get(url_contact, format='json')

        assert response.status_code == 403
        assert response.data['Status'] is False
        assert 'Error' in response.data

    def test_contact_post(self):
        """
        Проверка метода POST.
        Проверяет код HTTP-статуса, отсутсвие ошибок в данных ответа.
        Представление ContactView.
        """

        url_contact = reverse('user-contact')

        self.create_test_user()
        email = self.data['email']
        user = User.objects.get(email=email)
        token = Token.objects.get_or_create(user_id=user.id)[0].key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        data = {
            "city": "Samarkand",
            "street": "Lenina",
            "house": "24",
            "structure": "1",
            "building": "5",
            "apartment": "56",
            "phone": "+998 66 239 32 07"
        }

        response = self.client.post(url_contact, data=data)

        assert response.status_code == 201
        assert response.data['Status'] is True
        assert 'Error' not in response.data

    def test_post_contact_empty_data(self):
        """
        Проверка метода POST при незаполненных полях.
        Проверяет код HTTP-статуса,наличие ошибок в данных ответа.
        Представление ContactView.
        """

        url_contact = reverse('user-contact')

        self.create_test_user()
        email = self.data['email']
        user = User.objects.get(email=email)
        token = Token.objects.get_or_create(user_id=user.id)[0].key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        data = {
            "city": "Ivanteevka",
            "street": "Zarechnaya",
            "structure": "1",
            "building": "1",
            "phone": "8-800-555-35-35"
        }

        response = self.client.post(url_contact, data=data, format='json')

        assert response.status_code == 401
        assert response.data['Status'] is False
        assert 'Error' not in response.data

    def test_delete_contact(self):
        """
        Проверка метода DELETE.
        Проверяет status_code и наличие статуса True в данных ответа.
        Представление ContactView.
        """

        url_contact = reverse('user-contact')

        self.create_test_user()
        email = self.data['email']
        user = User.objects.get(email=email)
        token = Token.objects.get_or_create(user_id=user.id)[0].key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        data = {"items": "10"}

        response = self.client.delete(url_contact, data=data, format='json')

        assert response.status_code == 200

    def test_delete_contact_empty_data(self):
        """
        Проверка метода DELETE при незаполненных полях.
        Проверяет соответсвие status_code коду 404.
        Представление ContactView.
        """

        url_contact = reverse('user-contact')

        self.create_test_user()
        email = self.data['email']
        user = User.objects.get(email=email)
        token = Token.objects.get_or_create(user_id=user.id)[0].key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        data = {"items": ''}

        response = self.client.delete(url_contact, data=data, format='json')

        assert response.status_code == 400