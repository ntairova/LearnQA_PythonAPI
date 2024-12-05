from datetime import datetime
from allure_pytest.utils import allure_description
import allure
import pytest
import requests


from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):
    exclude_params = [("username"),
                      ("firstName"),
                      ("lastName"),
                      ("password"),
                      ("email"),
                      ]

    @allure.description("This test creates new user")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response,"id")

    @allure.description("This test checks that user can not be created with existing email")
    def test_create_user_with_existing_email(self):
         email = 'vinkotov@example.com'
         data = self.prepare_registration_data(email)
         response = MyRequests.post("/user/", data=data)

         Assertions.assert_code_status(response, 400)
         assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
             f"Unexpected response content {response.content}"

    @allure.description("This test checks that user can not be created with invalid email")
    def test_create_user_with_invalid_email(self): # Создание пользователя с некорректным email - без символа @
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response.content}"

    @allure.description("This test checks that user can not be created with short username")
    def test_create_user_with_short_username(self):  # Создание пользователя с очень коротким именем в один символ
        new_value = 'l'
        data = self.prepare_registration_data()
        data['username'] = new_value
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f"Unexpected response content {response.content}"

    @allure.description("This test creates user with long username (250 characters)")
    def test_create_user_with_long_username(self):  # Создание пользователя с очень длинным именем - длиннее 250 символов
        new_value = 'learnqa123'*25
        data = self.prepare_registration_data()
        data['username'] = new_value
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response,"id")

    @allure.description("This test checks different combinations with one empty field")
    @pytest.mark.parametrize('condition', exclude_params) # Создание пользователя без указания одного из полей - с помощью @parametrize необходимо проверить, что отсутствие любого параметра не дает зарегистрировать пользователя
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
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {condition}", \
            f"Unexpected response content {response.content}"








