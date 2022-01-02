from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.jwt import decodeJWT
from auth.bearer import JWTBearer
from dependencies import get_db
from cruds.histories import create_history, create_users_history
from cruds.users import read_user
from spotify import get_track_from_spotify

router = APIRouter()

@router.get("/tracks/recommend")
def read_fortune_track(db:Session=Depends(get_db)):
	data = get_track_from_spotify()
	create_history(db=db, spotify_song_id=data['id'])
	return data


@router.get("/tracks/recommend/authed")
def read_fortune_track(db:Session=Depends(get_db), jwt_payload=Depends(JWTBearer())):
	data = get_track_from_spotify()
	decoded_payload = decodeJWT(jwt_payload)
	user_instance = read_user(db=db, username=decoded_payload['username'])
	create_users_history(db=db, user_id=user_instance.id, spotify_song_id=data['id'])
	return data