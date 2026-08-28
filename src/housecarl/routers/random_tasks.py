# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
Defines the routes and handlers for the random tasks endpoint.

"""

import random
from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from housecarl.db import DatabaseSession
from housecarl.db.models import InspectionState, RandomTask, Task
from housecarl.schema import RandomTaskGenerate, RandomTaskItem

router = APIRouter()


def get_random_task_or_404(task_id: int, db: Session) -> RandomTask:
    """
    Returns a random task entry from the database.

    Args:
        task_id:
            Unique identifier for the task the random task entry belongs
            to.
        db:
            Database session to use when performing database operations.

    Raises:
        HTTPException:
            Raised if the task is not currently part of the random
            selection.

    """
    random_task = db.execute(
        select(RandomTask).where(RandomTask.task_id == task_id)
    ).scalar_one_or_none()
    if random_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Random task not found",
        )
    return random_task


def is_eligible(task: Task, now: datetime) -> bool:
    """
    Returns whether a task is eligible for random selection.

    A task is eligible if its state is not Good, or if the time since
    it was last performed exceeds its frequency.

    """
    last_performed = task.last_performed
    if last_performed.tzinfo is None:
        last_performed = last_performed.replace(tzinfo=UTC)
    return task.state != InspectionState.Good or now - last_performed > task.frequency


@router.get("", response_model=list[RandomTaskItem])
def all(db: DatabaseSession):
    """
    Returns list of all random tasks, sorted by number.

    """
    return db.execute(select(RandomTask).order_by(RandomTask.number)).scalars().all()


@router.post(
    "", response_model=list[RandomTaskItem], status_code=status.HTTP_201_CREATED
)
def generate(request: RandomTaskGenerate, db: DatabaseSession):
    """
    Generates a new set of random tasks.

    All existing random task entries are removed and replaced with a
    new random selection. Only tasks whose state is not Good, or whose
    time since last performed exceeds their frequency, are considered.

    """
    db.execute(delete(RandomTask))

    now = datetime.now(UTC)
    candidates = [
        task
        for task in db.execute(select(Task)).scalars().all()
        if is_eligible(task, now)
    ]

    selected = random.sample(candidates, k=min(request.count, len(candidates)))

    random_tasks = [
        RandomTask(number=number, task_id=task.id)
        for number, task in enumerate(selected, start=1)
    ]
    db.add_all(random_tasks)
    db.commit()
    for random_task in random_tasks:
        db.refresh(random_task)
    return random_tasks


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove(task_id: int, db: DatabaseSession):
    """
    Removes a task from the random selection.

    If another eligible task is available, it takes the removed task's
    slot in the selection.

    """
    random_task = get_random_task_or_404(task_id, db)
    number = random_task.number
    db.delete(random_task)
    db.flush()

    now = datetime.now(UTC)
    selected_task_ids = {
        row.task_id for row in db.execute(select(RandomTask)).scalars().all()
    }
    candidates = [
        task
        for task in db.execute(select(Task)).scalars().all()
        if task.id != task_id
        and task.id not in selected_task_ids
        and is_eligible(task, now)
    ]
    if candidates:
        replacement = random.choice(candidates)
        db.add(RandomTask(number=number, task_id=replacement.id))

    db.commit()


if __name__ == "__main__":
    pass
