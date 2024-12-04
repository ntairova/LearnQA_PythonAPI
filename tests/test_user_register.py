from datetime import datetime
import pytest
import requests


from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):

    def setup_method(self):
        base_part ="learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"
        self.values = [({'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': self.email}),
                  ({'password': '123', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': self.email}),
                  ({'password': '123', 'username': 'l', 'lastName': 'learnqa', 'email': self.email}),
                  ({'password': '123', 'username': 'l', 'firstName': 'learnqa', 'email': self.email}),
                  ({'password': '123', 'username': 'l', 'firstName': 'learnqa', 'lastName': self.email})
                  ]



    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName':'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response,"id")

    def test_create_user_with_existing_email(self):
         email = 'vinkotov@example.com'
         data = {
             'password': '123',
             'username': 'learnqa',
             'firstName':'learnqa',
             'lastName': 'learnqa',
             'email': email
         }

         response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

         Assertions.assert_code_status(response, 400)
         assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
             f"Unexpected response content {response.content}"

    def test_create_user_with_invalid_email(self): # Создание пользователя с некорректным email - без символа @
        email = 'vinkotovexample.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response.content}"
    def test_create_user_with_short_username(self):  # Создание пользователя с очень коротким именем в один символ
        data = {
            'password': '123',
            'username': 'l',
            'firstName':'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_long_username(self):  # Создание пользователя с очень длинным именем - длиннее 250 символов
        data = {
            'password': '123',
            'username': 'learnqa123'*25,
            'firstName':'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response,"id")

    # Создание пользователя без указания одного из полей - с помощью @parametrize необходимо проверить, что отсутствие любого параметра не дает зарегистрировать пользователя



    @pytest.mark.parametrize('value', self.values)
    def test_test(self, value):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=value)
        print('asdadadasd')
        print(response.status_code)








