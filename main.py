from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time



import  models
from models import *
from database import engine
from schemas import *
from routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="2128po", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Connected!')
        break
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print('Unable to connect to the database!')
        time.sleep(5)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)




