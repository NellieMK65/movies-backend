# 1. import fast api class
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
# this is an inbuilt package in python which will allow us to define the shape of POST and PATCH methods and also do validations
from pydantic import BaseModel
from models import get_db, Genre, Catalogue

# create and instance
app = FastAPI()

# allow network request from all servers
app.add_middleware(CORSMiddleware, allow_origins = ["*"])

# create routes to access resources
@app.get("/")
def read_root():
    return {"Hello": "World"}

class GenreSchema(BaseModel):
    name: str

# http://localhost:8000/genre -> POST -> create a single genre
@app.post("/genre")
def create_genre(genre: GenreSchema, session = Depends(get_db)):
    # check if the genre exists
    existing = session.query(Genre).filter(Genre.name == genre.name).first()

    if existing is None:
        # persist to db
        # 1. create an instance of the genre class(model) with the details
        new_genre = Genre(name = genre.name)
        # 2. add the instance to the transaction
        session.add(new_genre)
        # 3. commit the transaction
        session.commit()
        # return a message that the genre has been created
        return {"message": "Genre created successfully"}
    else:
        return {"message": "Genre already exists"}

# http://localhost:8000/genre -> GET -> retrieve all genres
@app.get("/genre")
def get_genres(session = Depends(get_db)):
    # use sql alchemy to retrieve all genres
    genres = session.query(Genre).all()
    return genres

# http://localhost:8000/genre/7 -> GET -> get a single genre
@app.get("/genre/{genre_id}")
def get_genre(genre_id):
    # retrieve a single genre using sqlalchemy
    # genre = db.query(Genre).filter(id == genre_id).first()
    # SELECT * FROM genre WHERE id = 7 LIMIT 1
    return {"id": genre_id}

# http://localhost:8000/genre/7 -> PACTH -> update a single genre
@app.patch("/genre/{genre_id}")
def update_genre(genre_id):
    return {}

# http://localhost:8000/genre/7 -> DELETE -> delete a single genre
@app.delete("/genre/{genre_id}")
def delete_genre(genre_id):
    return {}

