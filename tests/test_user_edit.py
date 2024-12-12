from datetime import datetime

import allure
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
     @allure.description("This test checks edit action for new created and authorized user")
     def test_edit_just_created_user(self):
         #Register
         register_data = self.prepare_registration_data()
         response1 =  MyRequests.post("/user/", data=register_data)


         Assertions.assert_code_status(response1, 200)
         Assertions.assert_json_has_key(response1,"id")

         email = register_data['email']
         username = register_data['username']
         first_name = register_data['firstName']
         password = register_data['password']
         user_id = self.get_json_value(response1, "id")

         #login
         login_data = {
            'email': email,
            'password': password
         }
         response2 = MyRequests.post("/user/login", data=login_data)


         auth_sid = self.get_cookie(response2, "auth_sid")
         token = self.get_header(response2,"x-csrf-token")

         #edit
         new_name = "Changed Name"
         response3 = MyRequests.put(f"/user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid},
                                  data={"firstName": new_name}
                                  )

         Assertions.assert_code_status(response3, 200)

         #get
         response4 = MyRequests.get(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

         Assertions.assert_json_value_by_name(
               response4,
              "firstName",
              new_name,
              'Wrong name of the user after edit'
              )

     @allure.description("This test checks that edit action can not be done without authorization")
     def test_edit_not_authorized_user(self): #- Попытаемся изменить данные пользователя, будучи неавторизованными
         #Register
         register_data = self.prepare_registration_data()
         response1 =  MyRequests.post("/user/", data=register_data)

         Assertions.assert_code_status(response1, 200)
         Assertions.assert_json_has_key(response1,"id")

         email = register_data['email']
         username = register_data['username']
         first_name = register_data['firstName']
         password = register_data['password']
         user_id = self.get_json_value(response1, "id")

         #edit
         new_email = "test@test.com"
         new_username = "Changed userame"
         new_firstname = "Changed Name"
         response2 = MyRequests.put(f"/user/{user_id}",
                                  data={"firstName": new_firstname, "username": new_username, "email": new_email}
                                  )
         Assertions.assert_code_status(response2, 400)
         Assertions.assert_json_value_by_name(
             response2,
             "error",
             "Auth token not supplied",
             f"Wrong response {response2.content}"
         )

     @allure.description("This test checks that authorized user can not edit another user")
     def test_edit_new_created_user_authorized_by_another_user(self): #- Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
         # Register
         # create 1st user
         data_user_for_edit = self.prepare_registration_data()
         response1 = MyRequests.post("/user/", data=data_user_for_edit)
         user_id_for_edit = self.get_json_value(response1, "id")

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

         # try to edit new created user logged as another user
         random_part = datetime.now().strftime("%m%d%Y%H%M%S.%f")
         new_email = f"test{random_part}@test.com"
         new_username = "Changed userame"
         new_firstname = "Changed Name"
         response4 = MyRequests.put(
             f"/user/{user_id_for_edit}",
             cookies={"auth_sid":auth_sid},
             headers={"x-csrf-token":token},
             data={"firstName": new_firstname, "username": new_username, "email": new_email}
             )

         Assertions.assert_code_status(response4, 400)
         Assertions.assert_json_value_by_name(
             response4,
           "error",
             "This user can only edit their own data.",
             f"Wrong response {response4.content}"
         )

     @allure.description("This test checks email format validation in edit action")
     def test_user_edit_update_email_to_invalid_email_format(self): #Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
         # Register
         register_data = self.prepare_registration_data()
         response1 = MyRequests.post("/user/", data=register_data)

         Assertions.assert_code_status(response1, 200)
         Assertions.assert_json_has_key(response1, "id")

         email = register_data['email']
         password = register_data['password']
         user_id = self.get_json_value(response1, "id")

         # login
         login_data = {
             'email': email,
             'password': password
         }
         response2 = MyRequests.post("/user/login", data=login_data)

         auth_sid = self.get_cookie(response2, "auth_sid")
         token = self.get_header(response2, "x-csrf-token")

         # try to edit new created user with invalid email
         new_email = "testexample.com"
         response3 = MyRequests.put(f"/user/{user_id}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid},
                                    data={"email": new_email}
                                    )

         Assertions.assert_code_status(response3, 400)
         Assertions.assert_json_value_by_name(
             response3,
             "error",
             "Invalid email format",
             f"Wrong response {response3.content}"
         )

     @allure.description("This test checks lenght of username field in one character in edit action")
     def test_user_edit_update_username_to_one_character_username(self):#- Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
         # Register
         register_data = self.prepare_registration_data()
         response1 = MyRequests.post("/user/", data=register_data)

         Assertions.assert_code_status(response1, 200)
         Assertions.assert_json_has_key(response1, "id")

         email = register_data['email']
         password = register_data['password']
         user_id = self.get_json_value(response1, "id")

         # login
         login_data = {
             'email': email,
             'password': password
         }
         response2 = MyRequests.post("/user/login", data=login_data)

         auth_sid = self.get_cookie(response2, "auth_sid")
         token = self.get_header(response2, "x-csrf-token")

         # try to edit new created user with invalid email
         new_username = "t"
         response3 = MyRequests.put(f"/user/{user_id}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid},
                                    data={"username": new_username}
                                    )

         Assertions.assert_code_status(response3, 400)
         Assertions.assert_json_value_by_name(
             response3,
             "error",
             "The value for field `username` is too short",
             f"Wrong response {response3.content}"
         )









