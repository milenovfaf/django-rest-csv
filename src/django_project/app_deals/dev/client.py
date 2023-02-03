import requests


url = "http://127.0.0.1:8000/api/deals/"


# file = {'file': ('deals.csv', open('dev/deals.csv', 'rb'))}
# response = requests.post(url, files=file)


file = 'dev/deals.csv'

response = requests.post(url, files={'file': open(file, 'rb')})

print(response.json())

if response.status_code == 200:
    print("File uploaded successfully")
else:
    print("Failed to upload the file")

print("Response status:", response.status_code)
response.raise_for_status()

