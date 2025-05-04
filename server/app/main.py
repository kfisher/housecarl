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
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

@app.get('/api/v1/rooms')
def read_rooms():
    """
    Gets a list of all rooms.

    """
    return []

@app.get('/api/v1/rooms/{room_id}')
def read_room(room_id: int):
    """
    Gets the details of a room whose id is `room_id`.

    """
    return {}

class CreateRoomRequest(BaseModel):
    """
    Specifies the data used to create a room.

    """
    name : str = Field(
        description='Name of the room.',
        examples=['Kitchen', 'Bathroom', 'Living Room']
    )

class CreateRoomResponse(BaseModel):
    """
    Specifies the data returned when a room is created.

    """
    id : int = Field(
        description='Id of the created room.'
    )
    name : str = Field(
        description='Name of the room.'
    )

@app.post('/api/v1/rooms', status_code=201)
def create_room(room: CreateRoomRequest) -> CreateRoomResponse:
    """
    Creates a new room.

    """
    return CreateRoomResponse()

class UpdateRoomRequest(BaseModel):
    """
    Specifies the data used to update a room.

    """
    name : str | None = Field(
        default=None,
        description='Name of the room.',
        examples=['Kitchen', 'Bathroom', 'Living Room']
    )

@app.patch('/api/v1/rooms/{room_id}', status_code=204)
def update_room(room_id: int, room: UpdateRoomRequest):
    """
    Updates the room whose id is `room_id`.

    """
    pass

@app.delete('/api/v1/rooms/{room_id}', status_code=204)
def delete_room(room_id: int):
    """
    Deletes the room whose id is `room_id`.

    """
    pass

if __name__ == '__main__':
    pass
