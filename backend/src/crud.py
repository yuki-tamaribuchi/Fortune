from sqlalchemy.orm import Session
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

def create_users_history(db:Session, user_id:int, spotify_song_id:str):
	db_users_history = UsersHistory(user_id=user_id, spotify_song_id=spotify_song_id, created_at=datetime.datetime.now())
	db.add(db_users_history)
	db.commit()
	db.refresh(db_users_history)
	return db_users_history