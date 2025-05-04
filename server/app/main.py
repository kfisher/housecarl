# ==============================================================================
# Copyright (c) 2025 Kevin Fisher
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program.  If not, see <https://www.gnu.org/licenses/>.
# ==============================================================================
"""
Defines the API (routes, request models, and response models).

"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import select

from . import db

class RoomDetails(BaseModel):
    """
    Contains the details for a room.

    """
    id: int = Field(
        description='The room\'s unique identifier.',
    )
    name: str = Field(
        description='The room\'s name.',
    )

class CreateRoomRequest(BaseModel):
    """
    Specifies the data used to create a room.

    """
    name : str = Field(
        description='Name of the room.',
        examples=['Kitchen', 'Bathroom', 'Living Room']
    )

class UpdateRoomRequest(BaseModel):
    """
    Specifies the data used to update a room.

    """
    name : str | None = Field(
        default=None,
        description='Name of the room.',
        examples=['Kitchen', 'Bathroom', 'Living Room']
    )

def is_empty_or_whitespace(s):
    """
    Returns True if the string is empty or contains only whitespace.
    Otherwise, returns False.

    """
    return not s.strip()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Defines the startup and shutdown logic for the application.

    """
    db.create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get('/api/v1/rooms', response_model_exclude_none=True)
def read_rooms(session: db.SessionDependency) -> list[RoomDetails]:
    """
    Gets a list of all rooms.

    """
    rooms = session.exec(select(db.Room)).all()
    return rooms

@app.get('/api/v1/rooms/{room_id}')
def read_room(room_id: int, session: db.SessionDependency) -> RoomDetails:
    """
    Gets the details of a room whose id is `room_id`.

    """
    room = session.get(db.Room, room_id)
    if room is None:
        raise HTTPException(status_code=404, detail='Room not found')
    return room

@app.post('/api/v1/rooms', response_model_exclude_none=True, status_code=201)
def create_room(
    room: CreateRoomRequest, 
    session: db.SessionDependency
) -> RoomDetails:
    """
    Creates a new room.

    """
    if is_empty_or_whitespace(room.name):
        raise HTTPException(
            status_code=422,
            detail='Room name cannot be empty or whitespace'
        )
    new_room = db.Room(name=room.name)
    session.add(new_room)
    session.commit()
    session.refresh(new_room)
    return new_room

@app.patch('/api/v1/rooms/{room_id}', status_code=204)
def update_room(
    room_id: int, 
    room: UpdateRoomRequest, 
    session: db.SessionDependency
):
    """
    Updates the room whose id is `room_id`.

    """
    room_db = session.get(db.Room, room_id)
    if room_db is None:
        raise HTTPException(status_code=404, detail='Room not found')
    if room.name is not None and is_empty_or_whitespace(room.name):
        raise HTTPException(
            status_code=422,
            detail='Room name cannot be empty or whitespace'
        )
    room_patch = room.model_dump(exclude_unset=True)
    room_db.sqlmodel_update(room_patch)
    session.add(room_db)
    session.commit()

@app.delete('/api/v1/rooms/{room_id}', status_code=204)
def delete_room(room_id: int, session: db.SessionDependency):
    """
    Deletes the room whose id is `room_id`.

    """
    room = session.get(db.Room, room_id)
    if room is None:
        raise HTTPException(status_code=404, detail='Room not found')
    session.delete(room)
    session.commit()

if __name__ == '__main__':
    pass
