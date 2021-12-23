from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


from crud import create_history, create_user, create_users_history, read_user, delete_user
from database import SessionLocal
from schemas import UserCreate, UserLogin, UserDelete
from auth_handler import signJWT, decodeJWT, authentication
from auth_bearer import JWTBearer

from spotify import get_track_from_spotify


#Base.metadata.create_all(bind=engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


app = FastAPI(title="Fortune")


origins = [
	'http://127.0.0.1:8000',
	'http://127.0.0.1:3000'
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*']
)



@app.get("/tracks/recommend")
def read_fortune_track(db:Session=Depends(get_db)):
	data = get_track_from_spotify()
	create_history(db=db, spotify_song_id=data['id'])
	return data


@app.get("/tracks/recommend/authed")
def read_fortune_track(db:Session=Depends(get_db), jwt_payload=Depends(JWTBearer())):
	data = get_track_from_spotify()
	decoded_payload = decodeJWT(jwt_payload)
	user_instance = read_user(db=db, username=decoded_payload['username'])
	create_users_history(db=db, user_id=user_instance.id, spotify_song_id=data['id'])
	return data


@app.post("/register")
def user_creation(user:UserCreate, db:Session=Depends(get_db)):
	user_instance = create_user(username=user.username, password=user.password, db=db)
	return signJWT(user_instance.username)


@app.post("/login")
def user_login(user:UserLogin, db:Session=Depends(get_db)):
	user_instance = authentication(db, user)
	if user_instance:
		return signJWT(user_instance.username)
	else:
		raise HTTPException(401)


@app.get("/users/{username}")
def user_read(username:str , db:Session=Depends(get_db)):
	user_instance = read_user(db=db, username=username)
	if user_instance:
		return user_instance
	else:
		raise HTTPException(404)


@app.delete("/users", status_code=status.HTTP_200_OK)
def user_delete(user:UserDelete, db:Session=Depends(get_db)):
	user_instance = authentication(db, user)
	if user_instance:
		delete_user(db, user_instance)
	else:
		raise HTTPException(401)