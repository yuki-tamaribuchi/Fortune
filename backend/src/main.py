from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal
from routers import users, histories


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

app.include_router(users.router)
app.include_router(histories.router)