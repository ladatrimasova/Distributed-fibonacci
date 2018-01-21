import requests
import time

for i in range(100):
    response = requests.put('http://localhost:2345/get_and_inc_fib', headers=dict(user_id='2'))
    print(response.text)
    time.sleep(2)