from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def test_delete_user_with_userId_equal_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.delete(
            f"/user/{user_id_from_auth_method}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
            )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_json_value_by_name(
            response2,
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            f"Wrong response {response2.content}"
        )

    def test_delete_new_authorized_user(self):
        #create user
        data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        #login
        response2 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response2, "user_id")
        #delete
        response3 = MyRequests.delete(
             f"/user/{user_id_from_auth_method}",
             cookies={"auth_sid": auth_sid},
             headers={"x-csrf-token": token}
        )

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_value_by_name(
            response3,
            "success",
            "!",
            f"Wrong response {response2.content}"
        )
        # try to find data for deleted user
        response4 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                headers={"x-csrf-token": token},
                                cookies={"auth_sid": auth_sid}
                                )
        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == f"User not found", \
            f"Unexpected response content {response4.content}"

    def test_delete_new_created_user_authorized_by_another_user(self):
        # create user
        data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=data)
        user_id_from_create_method = self.get_json_value(response1, "id")

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        #login
        data = {
             'email': 'vinkotov@example.com',
             'password': '1234'
        }

        response2 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response2, "user_id")

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            user_id_from_auth_method,
            f"Wrong response {response2.content}"
        )
        #delete
        response3 = MyRequests.delete(
             f"/user/{user_id_from_create_method}",
             cookies={"auth_sid": auth_sid},
             headers={"x-csrf-token": token}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            f"Wrong response {response2.content}")










