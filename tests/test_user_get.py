import requests
from requests import Response

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_not_key(response, 'firstName')
        Assertions.assert_json_has_not_key(response, 'lastName')
        Assertions.assert_json_has_not_key(response, 'email')

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
    #Homework Ex16: Запрос данных другого пользователя
    def test_get_user_details_auth_as_another_user(self):
        #create new user
        username_not_auth_user = 'Unauth User Name'
        data = self.prepare_registration_data()
        data['username'] = username_not_auth_user
        response1 =  MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1,"id")
        user_id_from_create_user_method = self.get_json_value(response1, "id")

        #login as existing user vinkotov@example.com
        data = {'email':'vinkotov@example.com',
               'password':'1234'}
        response2 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #try to get details for new_created user logged as another user:vinkotov@example.com
        response3 = MyRequests.get(f"/user/{user_id_from_create_user_method}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        Assertions.assert_json_has_key(response3, 'username')
        Assertions.assert_json_has_not_key(response3, 'firstName')
        Assertions.assert_json_has_not_key(response3, 'lastName')
        Assertions.assert_json_has_not_key(response3, 'email')
        Assertions.assert_json_value_by_name(
            response3,
            "username",
            username_not_auth_user,
            'Wrong username'
        )








