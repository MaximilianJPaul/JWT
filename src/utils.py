import json
import base64

class Header:
    def __init__(self, alg: str, typ: str):
        self.alg = alg
        self.typ = typ

    def json(self):
        header = {
            "alg": self.alg,
            "typ": self.typ,
        }

        return json.dumps(header)


class Payload:
    def __init__(self, claims):
        self.claims = claims

    def json(self):
        return json.dumps(self.claims)
    

def base64url_decode(input):
    rem = len(input) % 4
    if rem > 0:
        input += '=' * (4 - rem)
    return base64.urlsafe_b64decode(input)
