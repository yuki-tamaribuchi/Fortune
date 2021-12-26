from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies import get_db
from cruds.users import create_user, read_user, delete_user, update_user
from schemas import UserCreate, UserLogin, UserDelete, UserUpdate
from auth_handler import signJWT, decodeJWT, authentication
from auth_bearer import JWTBearer


router = APIRouter()


@router.post("/register/")
async def register_user(user:UserCreate, db:Session=Depends(get_db)):
	user_instance = create_user(db=db, username=user.username, password=user.password, handle=user.handle, profile_image=user.profile_image)
	if user_instance:
		return signJWT(user_instance.username)
	return HTTPException(409)


@router.post("/login/")
async def login_user(user:UserLogin, db:Session=Depends(get_db)):
	user_instance = authentication(db=db, user=user)
	if user_instance:
		return signJWT(user_instance.username)
	raise HTTPException(401)


@router.get("/users/")
async def myself_read(db:Session=Depends(get_db), jwt_payload=Depends(JWTBearer())):
	decoded_payload = decodeJWT(jwt_payload)
	user_instance = read_user(db=db, username=decoded_payload['username'])
	if user_instance:
		return user_instance
	else:
		raise HTTPException(404)


@router.get("/users/{username}")
async def user_read(username:str , db:Session=Depends(get_db)):
	user_instance = read_user(db=db, username=username)
	if user_instance:
		return user_instance
	else:
		raise HTTPException(404)


@router.post("/users/")
async def user_update(user_update_data:UserUpdate ,db:Session=Depends(get_db), jwt_payload=Depends(JWTBearer())):
	decoded_payload = decodeJWT(jwt_payload)
	user_updated_instance = update_user(db=db, username=decoded_payload['username'], user_update_data=user_update_data)


@router.delete("/users", status_code=status.HTTP_200_OK)
async def user_delete(user:UserDelete, db:Session=Depends(get_db)):
	user_instance = authentication(db, user)
	if user_instance:
		delete_user(db, user_instance)
	else:
		raise HTTPException(401)