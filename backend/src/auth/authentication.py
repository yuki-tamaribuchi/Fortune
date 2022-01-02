from utils import calc_hash
from cruds.users import read_user
from schemas import UserAuthenticate

def authentication(db, user:UserAuthenticate):
	user_instance = read_user(db, username=user.username)

	if user_instance:
		if not user_instance.is_active:
			return

		hashed_password = calc_hash(password=user.password, salt=bytes.fromhex(user_instance.salt)).hex()

		if hashed_password == user_instance.password:
			return user_instance
	return