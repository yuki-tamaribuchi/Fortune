import jwt
import os
import time
from typing import Dict


from crud import read_user
from schemas import UserAuthenticate
from utils import calc_hash

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


def authentication(db, user:UserAuthenticate):
	user_instance = read_user(db, username=user.username)

	if user_instance:
		if not user_instance.is_active:
			return

		hashed_password = calc_hash(password=user.password, salt=bytes.fromhex(user_instance.salt)).hex()

		if hashed_password == user_instance.password:
			return user_instance
	return