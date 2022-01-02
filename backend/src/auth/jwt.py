import jwt
import os
import time
from typing import Dict


#https://testdriven.io/blog/fastapi-jwt-auth/

JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')

def token_response(token:str):
	return {
		'access_token': token
	}


def signJWT(username:str) -> Dict[str, str]:
	payload = {
		'username': username,
		'expires': time.time() + 604800 #7days
	}
	token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

	return token_response(token)


def decodeJWT(token:str) -> dict:
	try:
		decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
		return decoded_token if decoded_token['expires'] >= time.time() else None
	except:
		return {}