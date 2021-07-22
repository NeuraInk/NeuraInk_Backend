import os
import requests
from time import sleep

# while(1):
backend_url = "http://localhost:8000"

file_path = "testphoto/"
file_name = "f_12.png"
bucket_name = "neuraink"

body = {
    "file_path": file_path,
    "file_name": file_name,
    "bucket_name": bucket_name
}
res = requests.post(backend_url + f"/process/", json=body)
res = res.json()
print(res)
#     for i in range(300):
#         print(i)
#         sleep(1)