from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import UploadFile

from models import User
from schemas import UserUpdate

#https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
def create_user(db:Session, username:str, password:str, handle:str, profile_image:str):
	from utils import hash_password

	salt, key = hash_password(password)

	try:
		db_user = User(
			username=username,
			password=key,
			salt=salt,
			handle=handle,
			profile_image=profile_image
		)
		db.add(db_user)
		db.commit()
		db.refresh(db_user)
		return db_user
	except SQLAlchemyError:
		db.rollback()
		


def update_user(db:Session, username:str, user_update_data:UserUpdate, profile_image:UploadFile):


	try:
		db.query(User).filter(User.username==username).update(
			{
				User.handle:user_update_data.handle
			}
		)
		db.commit()
		return True
	except SQLAlchemyError:
		db.rollback()

def update_user_profile_image(db:Session, username:str, profile_image_filename:str):
	try:
		db.query(User).filter(User.username==username).update(
			{
				User.profile_image:profile_image_filename
			}
		)
		db.commit()
		return True
	except SQLAlchemyError:
		db.rollback()

def delete_user(db:Session, username_instance):
	try:
		db.query(User).filter(User.id==username_instance.id).update({User.is_active:0})
		db.commit()
		return True
	except SQLAlchemyError:
		db.rollback()


def read_user(db:Session, username:str):
	statement = select(User).filter_by(username=username)
	try:
		result = db.execute(statement).first()
		if result:
			return result._asdict()['User']
		return
	except SQLAlchemyError:
		return