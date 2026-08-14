# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Defines the routes and handlers for the rooms endpoint.

"""

from fastapi import APIRouter, HTTPException, status

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from housecarl.db import DatabaseSession
from housecarl.db.models import Room
from housecarl.schema import RoomCreate, RoomDetails, RoomItem, RoomUpdate

def get_room_or_404(room_id: int, db: Session) -> Room:
    """
    Returns a room entry from the database.

    Args:
        room_id:
            Unique identifier for the desired room.
        db:
            Database session to use when performing database operations.

    Raises:
        HTTPException:
            Raised if a room does not exist with the provided database.

    """
    room = db.get(Room, room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Room not found',
        )
    return room


router = APIRouter()


@router.get('', response_model=list[RoomItem])
def all(db: DatabaseSession):
    """
    Returns list of all rooms.

    """
    return db.execute(select(Room)).scalars().all()


@router.get('/{room_id}', response_model=RoomDetails)
def details(room_id: int, db: DatabaseSession):
    """
    Returns the details for a room.

    """
    return get_room_or_404(room_id, db)


@router.post('', response_model=RoomItem, status_code=status.HTTP_201_CREATED)
def create(room: RoomCreate, db: DatabaseSession):
    """
    Creates a new room entry in the database.

    """
    db_room = Room(**room.model_dump())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


@router.patch('/{room_id}', response_model=RoomItem)
def update(room_id: int, room: RoomUpdate, db: DatabaseSession):
    """
    Updates an existing room in the database.

    """
    db_room = get_room_or_404(room_id, db)
    for key, value in room.model_dump(exclude_unset=True).items():
        setattr(db_room, key, value)
    db.commit()
    db.refresh(db_room)
    return db_room


@router.delete('/{room_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(room_id: int, db: DatabaseSession):
    """
    Deletes a room entry from the database and any associated tasks.

    """
    db_room = get_room_or_404(room_id, db)
    db.delete(db_room)
    db.commit()


if __name__ == '__main__':
    pass

