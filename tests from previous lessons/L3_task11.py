import pytest
import requests

def test_cookies():
    response = requests.post("https://playground.learnqa.ru/api/homework_cookie")
    print(dict(response.cookies))
    assert "HomeWork" in response.cookies and "hw_value" in response.cookies.get('HomeWork'), "invalid or empty cookies"

