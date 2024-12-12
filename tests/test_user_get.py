import allure
import requests
from requests import Response

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserGet(BaseCase):
    @allure.description("This test checks that only USERNAME is returned if user is not authorized")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_not_key(response, 'firstName')
        Assertions.assert_json_has_not_key(response, 'lastName')
        Assertions.assert_json_has_not_key(response, 'email')

    @allure.description("This test checks that user data is returned if user is authorized")
    def test_get_user_details_auth_as_same_user(self):
        data = {'email':'vinkotov@example.com',
               'password':'1234'}
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")


        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        expected_fields = ["username", "firstName", "lastName", "email"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This test checks that authorized user can NOT receive data of another user, except username")
    def test_get_user_details_auth_as_another_user(self):    #Homework Ex16: Запрос данных другого пользователя
        # create 1st user
        auth_user_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=auth_user_data)
        print(response1.status_code)
        print(response1.content)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = auth_user_data['email']
        password = auth_user_data['password']
        print(email)

        # login as 1st user
        data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        print(response2.status_code)

        # create 1st user
        data_user_for_return = self.prepare_registration_data()
        data_user_for_return['username'] = 'return_username'
        email = data_user_for_return['email']
        print(email)
        response3 = MyRequests.post("/user/", data=data_user_for_return)
        user_id_for_return = self.get_json_value(response3, "id")

        print(response3.status_code)
        print(response3.content)
        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, "id")

        #try to get details for new_created user logged as another user
        response4 = MyRequests.get(f"/user/{user_id_for_return}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        print(response4.status_code)
        Assertions.assert_json_has_key(response4, 'username')
        Assertions.assert_json_has_not_key(response4, 'firstName')
        Assertions.assert_json_has_not_key(response4, 'lastName')
        Assertions.assert_json_has_not_key(response4, 'email')
        Assertions.assert_json_value_by_name(
            response4,
            "username",
            data_user_for_return['username'],
            f"Wrong response {response4.content}"
        )








