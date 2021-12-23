from sqlalchemy.orm import Session
from sqlalchemy import select

from models import User

#https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
def create_user(db:Session, username:str, password:str):
	from utils import hash_password

	salt, key = hash_password(password)

	try:
		db_user = User(username=username, password=key, salt=salt)
		db.add(db_user)
		db.commit()
		db.refresh(db_user)
		return db_user
	except:
		return


def delete_user(db:Session, username_instance):
	try:
		db.query(User).filter(User.id==username_instance.id).update({User.is_active:0})
		db.commit()
		return True
	except:
		return False


def read_user(db:Session, username:str):
	statement = select(User).filter_by(username=username)
	try:
		result = db.execute(statement).first()._asdict()['User']
	except:
		result = None

	return result