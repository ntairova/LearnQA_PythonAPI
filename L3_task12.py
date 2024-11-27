import pytest
import requests

def test_header():
    response = requests.get("https://playground.learnqa.ru/api/homework_header")
    print(response.headers)
    assert "x-secret-homework-header" in response.headers and "Some secret value" in response.headers.get('x-secret-homework-header'), "invalid header"
