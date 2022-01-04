from os import environ


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


def save_image(image_object, path_and_filename):
	import boto3
	from botocore.exceptions import ClientError
	import os
	import logging


	s3_client = boto3.client(
		's3',
		aws_access_key_id=os.environ.get('AWS_S3_SECRET_ID'),
		aws_secret_access_key=os.environ.get('AWS_S3_SECRET_KEY')
	)

	try:
		response = s3_client.upload_fileobj(image_object, os.environ.get('AWS_S3_BUCKET'), path_and_filename)
	except ClientError as e:
		logging.error(e)
		return False
	return True

	