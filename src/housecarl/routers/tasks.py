# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Defines the routes and handlers for the tasks endpoint.

"""

from fastapi import APIRouter, HTTPException, status

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from housecarl.db import DatabaseSession
from housecarl.db.models import Task
from housecarl.routers.rooms import get_room_or_404
from housecarl.schema import TaskCreate, TaskDetails, TaskItem, TaskUpdate


def get_task_or_404(task_id: int, db: Session) -> Task:
    """
    Returns a task entry from the database.

    Args:
        task_id:
            Unique identifier for the desired task.
        db:
            Database session to use when performing database operations.

    Raises:
        HTTPException:
            Raised if a task does not exist with the provided database.

    """
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found',
        )
    return task


router = APIRouter()


@router.get('', response_model=list[TaskItem])
def all(db: DatabaseSession):
    """
    Returns list of all tasks.

    """
    return db.execute(select(Task)).scalars().all()


@router.get('/{task_id}', response_model=TaskDetails)
def details(task_id: int, db: DatabaseSession):
    """
    Returns the details for a task.

    """
    return get_task_or_404(task_id, db)


@router.post('', response_model=TaskItem, status_code=status.HTTP_201_CREATED)
def create(task: TaskCreate, db: DatabaseSession):
    """
    Creates a new task entry in the database.

    """
    get_room_or_404(task.room_id, db)
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.patch('/{task_id}', response_model=TaskItem)
def update(task_id: int, task: TaskUpdate, db: DatabaseSession):
    """
    Updates an existing task in the database.

    """
    db_task = get_task_or_404(task_id, db)
    updates = task.model_dump(exclude_unset=True)
    if 'room_id' in updates:
        get_room_or_404(updates['room_id'], db)
    for key, value in updates.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(task_id: int, db: DatabaseSession):
    """
    Deletes a task entry from the database and any associated tasks.

    """
    db_task = get_task_or_404(task_id, db)
    db.delete(db_task)
    db.commit()


if __name__ == '__main__':
    pass

