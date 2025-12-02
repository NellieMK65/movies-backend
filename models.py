#1 import the necessary packages
from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker # latest version

# create an engine which essentially is responsible for converting sql to python and vice versa
engine = create_engine("sqlite:///movies.db", echo=True)

# create session which allows us to interface with the db
Session = sessionmaker(bind=engine)

# for fastapi, we need to create a method that returns the session
def get_db():
    session = Session()
    try:
        # retuns the session which we can use to interact with the db via fastapi methods
        yield session
    finally:
        # this closes the connection to the db
        session.close()

# 2. Setup the base class from which all our models will inherit from
Base = declarative_base()

# Data Integrity (Correctness) - db constraints NOT NULL, UNIQUE

# 3. Start creating the schema
class Genre(Base):
    # we must the table name via the attribute __tablename__
    __tablename__ = "genre"

    # it must have at least one column
    id = Column(Integer(), primary_key=True)
    name = Column(Text(), nullable=False, unique=True)
    created_at = Column(DateTime, default = datetime.now())

class Catalogue(Base):
    __tablename__ = "catalogues"

    id = Column(Integer(), primary_key=True)
    name = Column(Text(), nullable=False)
    year = Column(Integer(), nullable=False)
    description = Column(Text(), nullable=False)
    genre_id = Column(Integer())
    like_count = Column(Integer(), nullable=False, default=0)
    duration = Column(Integer(), nullable=False) # we will store duration in minutes
    created_at = Column(DateTime, default = datetime.now())
