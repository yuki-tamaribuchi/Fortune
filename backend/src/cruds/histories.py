from sqlalchemy.orm import Session

import datetime

from models import History, UsersHistory

def create_history(db:Session, spotify_song_id:str):
	
	db_history = History(spotify_song_id=spotify_song_id, created_at=datetime.datetime.now())
	db.add(db_history)
	db.commit()
	db.refresh(db_history)
	return db_history

def create_users_history(db:Session, user_id:int, spotify_song_id:str):
	db_users_history = UsersHistory(user_id=user_id, spotify_song_id=spotify_song_id, created_at=datetime.datetime.now())
	db.add(db_users_history)
	db.commit()
	db.refresh(db_users_history)
	return db_users_history