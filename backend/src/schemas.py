from typing import Optional
from pydantic import BaseModel, constr

import datetime

class HistoryBase(BaseModel):
	spotify_song_id: str

class HistoryCreate(HistoryBase):
	pass

class History(HistoryBase):
	id: int
	created_at: datetime.datetime

	class Config:
		orm_mode = True

#https://stackoverflow.com/questions/61326020/how-can-i-set-max-string-field-length-constraint-in-pydantic
class UserBase(BaseModel):
	username: Optional[constr(max_length=32)]

class UserCreate(UserBase):
	password: str

class UserAuthenticate(UserBase):
	password: str

class UserLogin(UserAuthenticate):
	pass

class UserDelete(UserAuthenticate):
	pass

class User(UserBase):
	id: int
	is_active: bool
	password: str
	salt: str

	class Config:
		orm_mode = True

class UsersHitoryBase(BaseModel):
	spotify_song_id:str

class UsersHistoryCreate(UsersHitoryBase):
	pass

class UsersHistory(UsersHitoryBase):
	id:int
	user_id:int
	created_at:datetime.datetime