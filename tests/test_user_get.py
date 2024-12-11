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
        data_user_for_return = self.prepare_registration_data()
        data_user_for_return['username'] = 'return_username'
        response1 = MyRequests.post("/user/", data=data_user_for_return)
        user_id_for_return = self.get_json_value(response1, "id")


        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # create 2nd user
        auth_user_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=auth_user_data)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email = auth_user_data['email']
        password = auth_user_data['password']

        # login as 2nd user
        data = {
            'email': email,
            'password': password
        }

        response3 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")
        print(response3.status_code)

        #try to get details for new_created user logged as another user
        response3 = MyRequests.get(f"/user/{user_id_for_return}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        print(response3.status_code)
        Assertions.assert_json_has_key(response3, 'username')
        Assertions.assert_json_has_not_key(response3, 'firstName')
        Assertions.assert_json_has_not_key(response3, 'lastName')
        Assertions.assert_json_has_not_key(response3, 'email')
        Assertions.assert_json_value_by_name(
            response3,
            "username",
            data_user_for_return['username'],
            f"Wrong response {response3.content}"
        )








