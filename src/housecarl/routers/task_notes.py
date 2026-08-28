# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Defines the routes and handlers for the task notes endpoint.

"""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from housecarl.db import DatabaseSession
from housecarl.db.models import TaskNote
from housecarl.routers.tasks import get_task_or_404
from housecarl.schema import TaskNoteCreate, TaskNoteItem, TaskNoteUpdate


def get_task_note_or_404(note_id: int, db: Session) -> TaskNote:
    """
    Returns a task note entry from the database.

    Args:
        note_id:
            Unique identifier for the desired task note.
        db:
            Database session to use when performing database operations.

    Raises:
        HTTPException:
            Raised if a task note does not exist with the provided
            identifier.

    """
    note = db.get(TaskNote, note_id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task note not found",
        )
    return note


router = APIRouter()


@router.get("", response_model=list[TaskNoteItem])
def all(db: DatabaseSession, task_id: int | None = None):
    """
    Returns list of all task notes, sorted newest first.

    Args:
        task_id:
            If provided, restricts the results to notes belonging to
            the task with this identifier.

    """
    query = select(TaskNote).order_by(TaskNote.date.desc())
    if task_id is not None:
        query = query.where(TaskNote.task_id == task_id)
    return db.execute(query).scalars().all()


@router.get("/{note_id}", response_model=TaskNoteItem)
def details(note_id: int, db: DatabaseSession):
    """
    Returns the details for a task note.

    """
    return get_task_note_or_404(note_id, db)


@router.post("", response_model=TaskNoteItem, status_code=status.HTTP_201_CREATED)
def create(note: TaskNoteCreate, db: DatabaseSession):
    """
    Creates a new task note entry in the database.

    """
    get_task_or_404(note.task_id, db)
    db_note = TaskNote(**note.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@router.patch("/{note_id}", response_model=TaskNoteItem)
def update(note_id: int, note: TaskNoteUpdate, db: DatabaseSession):
    """
    Updates an existing task note in the database.

    """
    db_note = get_task_note_or_404(note_id, db)
    for key, value in note.model_dump(exclude_unset=True).items():
        setattr(db_note, key, value)
    db.commit()
    db.refresh(db_note)
    return db_note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(note_id: int, db: DatabaseSession):
    """
    Deletes a task note entry from the database.

    """
    db_note = get_task_note_or_404(note_id, db)
    db.delete(db_note)
    db.commit()


if __name__ == "__main__":
    pass
