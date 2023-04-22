'''
date: 0417
implement jwt
'''
import base64
import hmac
import json

import hashlib
import secrets
from datetime import datetime, timedelta

# input is encoded JSON
def base64url_encode(input: bytes):
    return base64.urlsafe_b64encode(input).decode('utf-8').replace('=', '')

def generator_jwt(payload_dic: dict, secret_key: str)-> str:
    '''
       :param payload: user name and expire time
       :param signature_key: password
       :return: a string of header.payload.signature
       '''
    header = {"typ": "JWT", "alg": "HS256"}
    payload['user_id']  = payload_dic['user_id']
    payload['exp'] = payload_dic['exp']

    # payload = {'user_id': user_id, "exp": expire_time}
    total_params = str(base64url_encode(json.dumps(header).encode()))+ '.' + str(base64url_encode(json.dumps(payload).encode()))

    signature = hmac.new(secret_key.encode(), total_params.encode(), hashlib.sha256).digest()
    token = total_params + '.' + str(base64url_encode(signature))
    # return format: '{header}.{payload}.{signature}'
    return token

# still has bug, please use https://kjur.github.io/jsrsasign/tool/tool_jwtveri.html verification url
def verify_jwt(token, secret_key):
    # header, payload, signature = token.split('.')
    # expected_signature = hmac.new(secret_key.encode(), f'{header}.{payload}'.encode(), digestmod='SHA256').digest()
    # expected_signature = base64url_encode(expected_signature).decode()

    header_b64, payload_b64, signature_b64 = token.split('.')
    header = json.loads(base64url_encode(header_b64 + '=' * (4 - len(header_b64) % 4)).decode('utf-8'))
    payload = json.loads(base64url_encode(payload_b64 + '=' * (4 - len(payload_b64) % 4)).decode('utf-8'))
    signature = base64url_encode(signature_b64 + '=' * (4 - len(signature_b64) % 4))
    expected_signature = hmac.new(secret_key.encode('utf-8'), (header + '.' + payload).encode('utf-8'), digestmod='sha256').digest()
    if signature != expected_signature:
        raise ValueError('Invalid signature')
    return json.loads(base64url_encode(payload))

# expire in 10 min
due_date = datetime.now() + timedelta(minutes=10)
expire_time = int(due_date.timestamp())

# Generate a JWT token
secret_key = secrets.token_urlsafe(32)
payload = {'user_id': 123, "exp": 600}

token = generator_jwt(payload, secret_key)
for i in token.split('.'):
    print(i)
# Verify the JWT token
# decoded_payload = verify_jwt(token, secret_key)
# assert decoded_payload == payload

