import requests
import time
import json

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
obj_st = response.json()
tn = obj_st["token"]
#print(response.text)

response1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params = {"token" : tn})
obj = response1.json()
print(obj["status"])

time.sleep(obj_st["seconds"])

response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params = {"token" : tn})
obj = response2.json()
print(obj["result"]["status"])