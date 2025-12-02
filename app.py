# 1. import fast api class
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
# this is an inbuilt package in python which will allow us to define the shape of POST and PATCH methods and also do validations
from pydantic import BaseModel
from models import get_db, Genre, Catalogue

# create and instance
app = FastAPI()

# allow network request from all servers
"""
-> by default the server only allows requests comming from the same port but
-> more often the frontend runs on a different port hence we need to allow this by setting
-> allow_origins = ["*"]
-> likewise, we also need to allow all the http methods by setting
-> allow_methods = ["*"]

-> This is not the best thing to do for security
"""
app.add_middleware(CORSMiddleware, allow_origins = ["*"], allow_methods=["*"])

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

class CatalogueSchema(BaseModel):
    name: str
    description: str
    year: int
    duration: int
    genre_id: int


# http://localhost:8000/catalogue -> POST -> to create catalogue
@app.post("/catalogue")
def create_catalogue(catologue: CatalogueSchema, session = Depends(get_db)):
    # 1. create instance of the model class imported from models.py
    new_catalogue = Catalogue(
        name=catologue.name,
        description=catologue.description,
        year=catologue.year,
        duration=catologue.duration,
        genre_id=catologue.genre_id
    )
    # 2. add this to session
    session.add(new_catalogue)
    # 3. save it by commiting the transaction
    session.commit()

    return {"message": "Movie added in successfully"}

# http://localhost:8000/catalogue -> GET -> retrieve all catalogues
@app.get("/catalogue")
def get_catalogues(session = Depends(get_db)):
    # use sql alchemy to retrieve all catalogues
    catalogues = session.query(Catalogue).all()
    return catalogues
