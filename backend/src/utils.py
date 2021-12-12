def hash_password(password:str):
	import hashlib
	import os


	salt = os.urandom(32)
	key = hashlib.pbkdf2_hmac(
		'sha256',
		password.encode('utf-8'),
		salt,
		100000
	)

	return salt.hex(), key.hex()