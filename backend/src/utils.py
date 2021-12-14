def calc_hash(password:str, salt:bytes):
	import hashlib

	key = hashlib.pbkdf2_hmac(
		'sha256',
		password.encode('utf-8'),
		salt,
		100000
	)

	return key

def hash_password(password:str):
	import os

	salt = os.urandom(32)
	key = calc_hash(password, salt)

	return salt.hex(), key.hex()