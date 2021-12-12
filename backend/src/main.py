from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from crud import create_history, create_user, create_users_history
from database import SessionLocal
from schemas import UserCreate

from spotify import get_track_from_spotify


#Base.metadata.create_all(bind=engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


app = FastAPI(title="Fortune")



@app.get("/tracks/recommend")
def read_fortune_track(db:Session=Depends(get_db)):

	data = get_track_from_spotify()
	create_history(db=db, spotify_song_id=data['id'])
	create_users_history(db=db, user_id=1, spotify_song_id=data['id'])
	return data


@app.post("/users/create")
def user_creation(user:UserCreate, db:Session=Depends(get_db)):
	user_instance = create_user(username=user.username, password=user.password, db=db)
	return user_instance