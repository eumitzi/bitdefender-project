import requests
file = {"_id": "1", "md5": "aaabbb"}
r = requests.get("http://127.0.0.1:5000/scan", params=file)
print(r.url)