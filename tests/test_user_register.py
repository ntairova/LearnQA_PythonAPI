from datetime import datetime
import pytest
import requests


from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):
    exclude_params = [("username"),
                      ("firstName"),
                      ("lastName"),
                      ("password"),
                      ("email"),
                      ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response,"id")

    def test_create_user_with_existing_email(self):
         email = 'vinkotov@example.com'
         data = self.prepare_registration_data(email)
         response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

         Assertions.assert_code_status(response, 400)
         assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
             f"Unexpected response content {response.content}"

    def test_create_user_with_invalid_email(self): # Создание пользователя с некорректным email - без символа @
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_short_username(self):  # Создание пользователя с очень коротким именем в один символ
        new_value = 'l'
        data = self.prepare_registration_data()
        data['username'] = new_value
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_long_username(self):  # Создание пользователя с очень длинным именем - длиннее 250 символов
        new_value = 'learnqa123'*25
        data = self.prepare_registration_data()
        data['username'] = new_value
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response,"id")

    # Создание пользователя без указания одного из полей - с помощью @parametrize необходимо проверить, что отсутствие любого параметра не дает зарегистрировать пользователя
    @pytest.mark.parametrize('condition', exclude_params)
    def test_with_excluded_param(self, condition):
        data = self.prepare_registration_data()
        if condition == "username":
            del data['username']
        elif condition == "firstName":
            del data['firstName']
        elif condition == "lastName":
            del data['lastName']
        elif condition == "password":
            del data['password']
        else:
            del data['email']
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {condition}", \
            f"Unexpected response content {response.content}"








