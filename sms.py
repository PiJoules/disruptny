import json
import requests

API_KEY = "95678560"
API_SECRET = "25715ea8b0f57094"

from_num = "12035298957"
FAKE_NUMBER = "FAKE_NUMBER"

url_base = "https://rest.nexmo.com/sms/json"


class NeximoException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg


def send_req(to_num, text):
    params = {
        'api_key': API_KEY,
        'api_secret': API_SECRET,
        'to': str(to_num),
        'from': from_num,
        'text': text
    }

    r = requests.get(url_base, params=params)
    if r.status_code == 200:
        resp = r.json()
        for msg in resp["messages"]:
            if int(msg["status"]) == 0:
                pass
            else:
                raise NeximoException(msg["status"], msg["error-text"])
    else:
        raise NeximoException(r,status_code, "Network error")


def send_many(targets, text):
    for target in targets:
        send_req(target, text)


if __name__ == "__main__":
    send_req("17325134403", "Test msg")
    #send_req("15164264399", "Test msg")
