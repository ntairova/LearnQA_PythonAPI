import requests
from requests import request

md = ["get", "post", "delete", "put"]
prm = ["GET", "POST", "DELETE", "PUT"]

#1st task -- вывод "Wrong method provided"
response = request(method=md[0], url="https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

#2nd task -- пустой вывод
response = request(method="HEAD", url="https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": "HEAD"})
print(response.text)
response = requests.head(url="https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

#3rd task -- вывод {"success":"!"}
response = request(method=md[0], url="https://playground.learnqa.ru/ajax/api/compare_query_type", params= {"method": prm[0]})
print(response.text)

#4th task
for i in range(len(md)):
    for k in range(len(prm)):
        if md[i] == 'get':
           response = request(method=md[i], url = "https://playground.learnqa.ru/ajax/api/compare_query_type", params= {"method": prm[k]})
           if md[i] == prm[k].lower() and response.text == 'Wrong method provided':
               print(md[i], prm[k], response.text)
           elif md[i] != prm[k].lower() and response.text != 'Wrong method provided':
               print(md[i], prm[k], response.text)
           else:
               pass
        else:
             response = request(method=md[i], url="https://playground.learnqa.ru/ajax/api/compare_query_type",
                            data={"method": prm[k]})
             if md[i] == prm[k].lower() and response.text == 'Wrong method provided':
                 print(md[i], prm[k], response.text)
             elif md[i] != prm[k].lower() and response.text != 'Wrong method provided':
                 print(md[i], prm[k], response.text)
             else:
                 pass