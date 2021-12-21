from sqlalchemy.orm import Session
from sqlalchemy import select
import datetime

from models import History, User, UsersHistory

def create_history(db:Session, spotify_song_id:str):
	

	db_history = History(spotify_song_id=spotify_song_id, created_at=datetime.datetime.now())
	db.add(db_history)
	db.commit()
	db.refresh(db_history)
	return db_history


#https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
def create_user(db:Session, username:str, password:str):
	from utils import hash_password

	salt, key = hash_password(password)

	db_user = User(username=username, password=key, salt=salt)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user


def delete_user(db:Session, username_instance):
	try:
		db.query(User).filter(User.id==username_instance.id).update({User.is_active:0})
		db.commit()
		return True
	except:
		return False


def read_user(db:Session, username:str):
	statement = select(User).filter_by(username=username)
	try:
		result = db.execute(statement).first()._asdict()['User']
	except:
		result = None

	return result

def create_users_history(db:Session, user_id:int, spotify_song_id:str):
	db_users_history = UsersHistory(user_id=user_id, spotify_song_id=spotify_song_id, created_at=datetime.datetime.now())
	db.add(db_users_history)
	db.commit()
	db.refresh(db_users_history)
	return db_users_history