# 1. import fast api class
from fastapi import FastAPI

# create and instance
app = FastAPI()

# create routes to access resources
@app.get("/")
def read_root():
    return {"Hello": "World"}

# http://localhost:8000/genre -> POST -> create a single genre
@app.post("/genre")
def create_genre():
    # Use sql alchemy to create the records
    return {"message": "Genre created successfully"}

# http://localhost:8000/genre -> GET -> retrieve all genres
@app.get("/genre")
def get_genres():
    # use sql alchemy to retrieve all genres
    return []

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

