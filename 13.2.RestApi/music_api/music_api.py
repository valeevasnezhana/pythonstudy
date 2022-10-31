from json import JSONDecodeError

from fastapi import FastAPI, Request, HTTPException, status
from pydantic import BaseModel, ValidationError, validator
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict

from string import ascii_letters, digits
from random import choices


def ids_generator_from_n(n: int):
    while True:
        yield n
        n += 1


id_generator = ids_generator_from_n(1)

tokens: List[str] = []


def create_token() -> str:
    token_ = ''.join(choices(ascii_letters + digits, k=40))
    tokens.append(token_)
    return token_


def validate_token(request: Request) -> Optional[JSONResponse]:
    if "x-token" not in request.headers:
        return JSONResponse(
            status_code=401,
            content={"detail": "Missing token"}
        )
    if request.headers["x-token"] not in tokens:
        return JSONResponse(
            status_code=401,
            content={"detail": "Incorrect token"}
        )
    return None


class User(BaseModel):
    name: str
    age: int


class TrackInfo(BaseModel):
    name: str
    artist: str
    year: Optional[int]
    genres: Optional[List[str]]

    def content(self):
        return {
            "name": self.name,
            "artist": self.artist,
            "year": self.year,
            "genres": self.genres if self.genres else []
        }

    def main_content(self):
        return {
            "name": self.name,
            "artist": self.artist
        }


tracks: Dict[int, TrackInfo] = {}


app = FastAPI()


@app.post("/api/v1/registration/register_user")
async def register_user(request: Request):
    json_content = await request.json()
    user = User.parse_obj(json_content)
    return JSONResponse(
        status_code=200,
        content={'token': create_token()}
    )


@app.post("/api/v1/tracks/add_track")
async def add_track(request: Request):
    token_error_response = validate_token(request)
    if token_error_response is not None:
        return token_error_response
    json_content = await request.json()
    try:
        track = TrackInfo.parse_obj(json_content)
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content={'detail': str(e)}
        )
    track_id = next(id_generator)
    tracks[track_id] = track
    return JSONResponse(
        status_code=201,
        content={"track_id": track_id}
    )


@app.delete("/api/v1/tracks/{track_id}")
async def delete_track(request: Request, track_id: int):
    vt = validate_token(request)
    if vt:
        return vt
    if track_id not in tracks.keys():
        return JSONResponse(
            status_code=404,
            content={"detail": "Invalid track_id"}
        )
    tracks.pop(track_id)
    return JSONResponse(
        status_code=200,
        content={"status": "track removed"}
    )


@app.get('/api/v1/tracks/all')
async def get_all_tracks(request: Request):
    vt = validate_token(request)
    if vt:
        return vt
    output_list = [track.content() for track in tracks.values()]
    return JSONResponse(
        status_code=200,
        content=output_list
    )


@app.get('/api/v1/tracks/search')
async def search_track(
        request: Request,
        name: Optional[str] = None,
        artist: Optional[str] = None,
):
    vt = validate_token(request)
    if vt:
        return vt

    if not name and not artist:
        return JSONResponse(
            status_code=422,
            content={"detail": "You should specify at least one search argument"}
        )
    output_list = []

    if name is not None and artist is not None:
        for track_id, track in tracks.items():
            if track.name == name and track.artist == artist:
                output_list.append(track_id)
    elif name is not None:
        for track_id, track in tracks.items():
            if track.name == name:
                output_list.append(track_id)
    elif artist is not None:
        for track_id, track in tracks.items():
            if track.artist == artist:
                output_list.append(track_id)

    return JSONResponse(
        status_code=200,
        content={'track_ids': output_list}
    )


@app.get("/api/v1/tracks/{track_id}")
async def get_track_main_info(request: Request, track_id: int):
    vt = validate_token(request)
    if vt:
        return vt
    if track_id not in tracks.keys():
        return JSONResponse(
            status_code=404,
            content={"detail": "Invalid track_id"}
        )
    return JSONResponse(
        status_code=200,
        content=tracks[track_id].main_content()
    )
