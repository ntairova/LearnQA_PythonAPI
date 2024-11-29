import requests
import pytest

class TestHeaders:
    values = [
        ({"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
         "platform": "Mobile", 'browser': 'No', 'device': 'Android'}),
        ({"User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
         "platform": "Mobile", "browser": "Chrome", "device": "iOS"}),
        ({"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
         "platform": "Googlebot", "browser": "Unknown", "device": "Unknown"}),
        ({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
         "platform":"Web", "browser": "Chrome", "device": "No"}),
        ({"User-Agent": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
         "platform": "Mobile", "browser": "No", "device": "iPhone"})
    ]


    @pytest.mark.parametrize('value', values)
    def test_headers(self, value):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        header =  {"User-Agent":value["User-Agent"]}

        response = requests.get(url, headers = header)
        platform_from_response = response.json()["platform"]
        browser_from_response = response.json()["browser"]
        device_from_response = response.json()["device"]
        print(platform_from_response, browser_from_response, device_from_response)
        assert platform_from_response == value["platform"] and browser_from_response == value["browser"] and device_from_response == value["device"], f"error  for {header}"

