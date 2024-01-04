import secrets
from jwt import JWT

key_length = 32

# Generate a random key
secret_key = secrets.token_bytes(key_length)


header = {
    "alg": "HS256",
    "typ": "JWT"
}

payload = {
    "username": "qwerty",
    "email": "qwertyh@gmail.com",
    "password": "qwerty12345"
}

def main():
    jwt_token = JWT(header, payload, secret=secret_key)
    print(jwt_token.encode())
    print(jwt_token.decode())
    

if __name__ == '__main__':
    main()