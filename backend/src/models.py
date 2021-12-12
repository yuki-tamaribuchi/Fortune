from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, String

from database import Base

class History(Base):
	__tablename__ = "histories"

	id = Column(Integer, primary_key=True, index=True)
	spotify_song_id = Column(String(length=22), unique=False, index=True)
	created_at = Column(DateTime)

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String(length=32))
	password = Column(String(length=64))
	salt = Column(String(length=64))
	is_active = Column(Boolean, default=True)

class UsersHistory(Base):
	__tablename__ = "users_histories"

	id = Column(Integer, primary_key=True, index=True)
	spotify_song_id = Column(String(length=22), unique=False)
	user_id = Column(Integer, ForeignKey('users.id'))
	created_at = Column(DateTime)
