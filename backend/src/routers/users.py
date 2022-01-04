from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session

from dependencies import get_db
from cruds.users import create_user, read_user, delete_user, update_user
from schemas import UserCreate, UserLogin, UserDelete, UserUpdate
from auth.jwt import signJWT, decodeJWT
from auth.authentication import authentication
from auth.bearer import JWTBearer
from utils import save_image


router = APIRouter()


@router.post("/register/")
async def register_user(user:UserCreate, db:Session=Depends(get_db)):
	user_instance = create_user(db=db, username=user.username, password=user.password, handle=user.handle, profile_image=user.profile_image)
	if user_instance:
		return signJWT(user_instance.username)
	raise HTTPException(409)


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
async def user_update(user_update_data:UserUpdate, profile_image: UploadFile=File(None), db:Session=Depends(get_db), jwt_payload=Depends(JWTBearer())):
	decoded_payload = decodeJWT(jwt_payload)
	user_updated_instance = update_user(db=db, username=decoded_payload['username'], user_update_data=user_update_data, profile_image=profile_image)


@router.post("/users/image")
async def user_update_profile_image(profile_image:UploadFile=File(...), db:Session=Depends(get_db), jwt_payload=Depends(JWTBearer())):
	print(profile_image.content_type)
	if profile_image.content_type == 'image/jpeg' or profile_image.content_type == 'image/png':
		if profile_image.content_type == 'image/jpeg':
			ext = '.jpeg'
		else:
			ext = '.png'

		decoded_payload = decodeJWT(jwt_payload)
		path = 'images/profile/'
		filename = decoded_payload['username'] + ext
		path_and_filename = path + filename
		if save_image(image_object=profile_image.file, path_and_filename=path_and_filename):
			return
		raise HTTPException(409)
	raise HTTPException(422)

	


@router.delete("/users", status_code=status.HTTP_200_OK)
async def user_delete(user:UserDelete, db:Session=Depends(get_db)):
	user_instance = authentication(db, user)
	if user_instance:
		delete_user(db, user_instance)
	else:
		raise HTTPException(401)