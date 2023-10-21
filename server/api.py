# Import des bibliothèques
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models
from pydantic import BaseModel
from .database import SessionLocal, engine

# Association de la variable app à une instance de la classe FastAPI
app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# Import des modèles de base de données
class ArtistBase(BaseModel):
    artistId: int
    name: str


class AlbumBase(BaseModel):
    albumId: int
    title: str
    artistId: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Requète get pour
@app.get("/artists/{name}", status_code=status.HTTP_200_OK)
async def read_artists(name: str, db: Session = Depends(get_db)):
    query = f"%{name}%"
    artist = db.query(models.Artist).where(models.Artist.name.like(query)).all()
    if artist is None:
        raise HTTPException(status_code=404, detail="Artist Name not in Database")
    return artist


@app.get("/albums/{artistId}", status_code=status.HTTP_200_OK)
async def read_albums(artistId: int, db: Session = Depends(get_db)):
    albums = db.query(models.Album).where(models.Album.artistId == artistId).all()
    if albums is None:
        raise HTTPException(
            status_code=404,
            detail="This artist id does not exist or have no albums in database",
        )
    return albums


@app.get("/tracks/{albumId}", status_code=status.HTTP_200_OK)
async def read_tracks(albumId: int, db: Session = Depends(get_db)):
    tracks = db.query(models.Track).where(models.Track.albumId == albumId).all()
    if tracks is None:
        raise HTTPException(
            status_code=404,
            detail="This albumid has no tracks connected to, check your album id",
        )
    return tracks
