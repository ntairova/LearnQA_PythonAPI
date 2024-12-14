import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests



@allure.epic("Deletion cases")
@allure.label("owner", "Nelya Tairova")
class TestUserDelete(BaseCase):
    @allure.description("This test checks that admin user can not be deleted")
    def test_delete_user_with_userId_equal_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step(f"Login as admin user {data['email']}"):
            response1 = MyRequests.post("/user/login", data=data)
            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step(f"Try do delete admin user"):
            response2 = MyRequests.delete(
            f"/user/{user_id_from_auth_method}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
            )

        with allure.step(f"Response status code = {response2.status_code}, response message={response2.content}"):
            Assertions.assert_code_status(response2, 400)
            Assertions.assert_json_value_by_name(
                response2,
                "error",
                "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
                f"Wrong response {response2.content}"
            )

    @allure.description("This test checks that auth user can be deleted")
    def test_delete_new_authorized_user(self):
        #create user
        with allure.step("Create user"):
            data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")
        #login
        with allure.step(f"Login as new user={data['username']}"):
            response2 = MyRequests.post("/user/login", data=data)
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response2, "user_id")
        #delete
        with allure.step(f"Login as new user={user_id_from_auth_method}"):
            response3 = MyRequests.delete(
                 f"/user/{user_id_from_auth_method}",
                 cookies={"auth_sid": auth_sid},
                 headers={"x-csrf-token": token}
            )

        with allure.step(f"Response status code = {response3.status_code}, response message={response3.content}"):
            Assertions.assert_code_status(response3, 200)
            Assertions.assert_json_value_by_name(
                response3,
                "success",
                "!",
                f"Wrong response {response2.content}"
            )
        # try to find data for deleted user
        with allure.step(f"Try to find deleted user ={user_id_from_auth_method}"):
            response4 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}
                                )
        with allure.step(f"Response status code = {response4.status_code}, response message={response4.content}"):
            Assertions.assert_code_status(response4, 404)
            assert response4.content.decode("utf-8") == f"User not found", \
                f"Unexpected response content {response4.content}"

    @allure.description("This test checks that authorized user can not delete another user")
    @allure.severity(severity_level='critical')
    def test_delete_new_created_user_authorized_by_another_user(self):
        with allure.step("Step1 - Create first user"):
            # create 1st user
            data_1st_user = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=data_1st_user)
            user_id_from_1st_create_method = self.get_json_value(response1, "id")

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

        with allure.step("Step2 - Create second user"):
            #create 2nd user
            second_user_data = self.prepare_registration_data()
            response2 = MyRequests.post("/user/", data=second_user_data)

            Assertions.assert_code_status(response2, 200)
            Assertions.assert_json_has_key(response2, "id")

            email = second_user_data['email']
            password = second_user_data['password']

        with allure.step(f"Step3 - Login as a second user with email = {email}"):
            #login as 2nd user
            data = {
                'email': email,
                'password':password
            }

            response3 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response3, "auth_sid")
            token = self.get_header(response3, "x-csrf-token")

        #delete
        with allure.step(f"Try to delete non authorized user = {user_id_from_1st_create_method}"):
            response4 = MyRequests.delete(
                  f"/user/{user_id_from_1st_create_method}",
                  cookies={"auth_sid": auth_sid},
                  headers={"x-csrf-token": token}
            )

        with allure.step(f"Response status code = {response4.status_code}, response message={response4.content}"):
            Assertions.assert_code_status(response4, 400)
            Assertions.assert_json_value_by_name(
                 response4,
                 "error",
                 "This user can only delete their own account.",
                 f"Wrong response {response4.content}"
            )
